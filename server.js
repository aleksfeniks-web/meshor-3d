const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Increase body size limit for large base64 image uploads
app.use(express.json({ limit: '50mb' }));

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// Serve index.html for the root route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Proxy POST requests to Replicate to bypass CORS
app.post('/api/replicate/models/:owner/:model/predictions', async (req, res) => {
    const { owner, model } = req.params;
    const authHeader = req.headers['authorization'];
    
    if (!authHeader) {
        return res.status(401).json({ detail: "Missing Authorization header" });
    }

    try {
        const response = await fetch(`https://api.replicate.com/v1/models/${owner}/${model}/predictions`, {
            method: 'POST',
            headers: {
                'Authorization': authHeader,
                'Content-Type': 'application/json',
                'Prefer': 'wait'
            },
            body: JSON.stringify(req.body)
        });

        const data = await response.json();
        res.status(response.status).json(data);
    } catch (error) {
        console.error('Error proxying prediction creation:', error);
        res.status(500).json({ detail: error.message });
    }
});

// Proxy GET requests to check prediction status
app.get('/api/replicate/predictions/:id', async (req, res) => {
    const { id } = req.params;
    const authHeader = req.headers['authorization'];

    if (!authHeader) {
        return res.status(401).json({ detail: "Missing Authorization header" });
    }

    try {
        const response = await fetch(`https://api.replicate.com/v1/predictions/${id}`, {
            method: 'GET',
            headers: {
                'Authorization': authHeader
            }
        });

        const data = await response.json();
        res.status(response.status).json(data);
    } catch (error) {
        console.error('Error proxying prediction status check:', error);
        res.status(500).json({ detail: error.message });
    }
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`🔮 Meshor 3D running on port ${PORT}`);
    console.log(`   http://localhost:${PORT}`);
});
