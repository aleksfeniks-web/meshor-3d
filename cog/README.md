# aleksfeniks-web/2dto3d — Cog Model

Converts 2D images to 3D meshes using **TripoSR** (Stability AI).

## How to Deploy to Replicate

### Prerequisites
- Linux machine with **NVIDIA GPU** (T4 or better)
- Docker installed
- [Cog](https://cog.run) installed:
  ```bash
  sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_Linux_x86_64
  sudo chmod +x /usr/local/bin/cog
  ```

### Steps

```bash
# 1. Clone repo and enter the cog directory
git clone https://github.com/aleksfeniks-web/meshor-3d.git
cd meshor-3d/cog

# 2. Test locally
cog predict -i image=@test_image.png

# 3. Login to Replicate
cog login

# 4. Push to your model
cog push r8.im/aleksfeniks-web/2dto3d
```

### API Usage (after push)

```python
import replicate

output = replicate.run(
    "aleksfeniks-web/2dto3d",
    input={
        "image": open("photo.jpg", "rb"),
        "output_format": "glb",
        "do_remove_background": True,
        "mc_resolution": 256,
        "foreground_ratio": 0.85
    }
)
print(output)  # URL to the 3D model file
```

### Inputs

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `image` | File | required | Input image (JPG, PNG, WEBP) |
| `output_format` | string | `glb` | Output format: `glb` or `obj` |
| `do_remove_background` | bool | `true` | Remove background before processing |
| `foreground_ratio` | float | `0.85` | Foreground size ratio (0.5-1.0) |
| `mc_resolution` | int | `256` | Marching cubes resolution (32/64/128/256) |

### Output
Returns a 3D mesh file (GLB or OBJ) with vertex colors.
