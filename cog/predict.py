"""
Predictor for aleksfeniks-web/2dto3d
Converts 2D images to 3D meshes using TripoSR.
"""

import os
import sys
import tempfile
import time
from typing import Optional

import numpy as np
import torch
from cog import BasePredictor, Input, Path
from huggingface_hub import hf_hub_download
from PIL import Image

# Ensure local tsr folder is importable
sys.path.append(os.path.abspath("."))

# Dynamic runtime patch to replace compiled torchmcubes with scikit-image
try:
    import tsr.models.isosurface
    def marching_cubes_skimage(level_tensor, threshold=0.0):
        from skimage import measure
        import torch
        level_np = level_tensor.detach().cpu().numpy()
        verts, faces, _, _ = measure.marching_cubes(level_np, level=threshold)
        v_pos = torch.from_numpy(verts.copy()).float()
        t_pos_idx = torch.from_numpy(faces.copy()).long()
        return v_pos, t_pos_idx
    tsr.models.isosurface.marching_cubes = marching_cubes_skimage
    print("✅ Successfully patched TripoSR marching_cubes to use scikit-image")
except Exception as e:
    print(f"⚠️ Failed to patch marching_cubes: {e}")


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load TripoSR model into memory for fast inference."""
        print("🔮 Loading TripoSR model...")
        start = time.time()

        # Import TripoSR components
        from tsr.system import TSR

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Download and load the pretrained TripoSR model
        self.model = TSR.from_pretrained(
            "stabilityai/TripoSR",
            config_name="config.yaml",
            weight_name="model.ckpt",
        )
        self.model.renderer.set_chunk_size(8192)
        self.model.to(self.device)

        # Import rembg for background removal
        from rembg import new_session
        self.rembg_session = new_session("u2net")

        elapsed = time.time() - start
        print(f"✅ Model loaded in {elapsed:.1f}s on {self.device}")

    def _remove_background(self, image: Image.Image) -> Image.Image:
        """Remove background from image using rembg."""
        from rembg import remove
        return remove(image, session=self.rembg_session)

    def _preprocess_image(
        self,
        image: Image.Image,
        do_remove_background: bool,
        foreground_ratio: float,
    ) -> Image.Image:
        """Preprocess image: remove background, center, and resize to 512x512."""
        if do_remove_background:
            image = self._remove_background(image)

        # Ensure RGBA
        image = image.convert("RGBA")

        # Find bounding box of non-transparent pixels
        alpha = np.array(image)[:, :, 3]
        rows = np.any(alpha > 0, axis=1)
        cols = np.any(alpha > 0, axis=0)

        if not rows.any() or not cols.any():
            # Fallback: return white-centered image
            result = Image.new("RGB", (512, 512), (255, 255, 255))
            return result

        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]

        # Crop to bounding box
        image = image.crop((cmin, rmin, cmax + 1, rmax + 1))

        # Calculate target size with foreground ratio
        max_dim = max(image.size)
        target_size = int(max_dim / foreground_ratio)

        # Create centered image on white background
        result = Image.new("RGBA", (target_size, target_size), (255, 255, 255, 255))
        paste_x = (target_size - image.size[0]) // 2
        paste_y = (target_size - image.size[1]) // 2
        result.paste(image, (paste_x, paste_y), image)

        # Resize to 512x512 and convert to RGB
        result = result.resize((512, 512), Image.LANCZOS)
        result = result.convert("RGB")

        return result

    def predict(
        self,
        image: Path = Input(
            description="Input image to convert to 3D model (JPG, PNG, WEBP)"
        ),
        output_format: str = Input(
            description="Output 3D format",
            choices=["glb", "obj"],
            default="glb",
        ),
        do_remove_background: bool = Input(
            description="Remove background from image before processing",
            default=True,
        ),
        foreground_ratio: float = Input(
            description="Ratio of foreground size to image size (0.5-1.0)",
            ge=0.5,
            le=1.0,
            default=0.85,
        ),
        mc_resolution: int = Input(
            description="Marching cubes resolution for mesh extraction",
            choices=[32, 64, 128, 256],
            default=256,
        ),
    ) -> Path:
        """Convert a 2D image to a 3D mesh."""
        print(f"📸 Processing image: {image}")
        start = time.time()

        # Load and preprocess image
        input_image = Image.open(str(image))
        processed_image = self._preprocess_image(
            input_image, do_remove_background, foreground_ratio
        )

        print(f"🧠 Running TripoSR inference...")

        # Run the model
        with torch.no_grad():
            scene_codes = self.model([processed_image], device=self.device)

        print(f"🔨 Extracting mesh (resolution={mc_resolution})...")

        # Extract mesh
        meshes = self.model.extract_mesh(
            scene_codes,
            has_vertex_color=True,
            resolution=mc_resolution,
        )

        mesh = meshes[0]

        # Export to requested format
        output_dir = tempfile.mkdtemp()
        output_path = os.path.join(output_dir, f"output.{output_format}")

        if output_format == "glb":
            mesh.export(output_path)
        elif output_format == "obj":
            mesh.export(output_path)

        elapsed = time.time() - start
        print(f"✅ Done in {elapsed:.1f}s → {output_format.upper()}")

        return Path(output_path)
