const express = require('express');
const path = require('path');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 8080;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname)));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/api/generate', async (req, res) => {
    const { prompt } = req.body;

    if (!prompt) {
        return res.status(400).json({ error: 'Prompt is required' });
    }

    console.log(`Generating image for prompt: ${prompt}`);

    try {
        // RunPod API details
        const RUNPOD_API_KEY = process.env.RUNPOD_API_KEY;
        const RUNPOD_ENDPOINT_ID = process.env.RUNPOD_ENDPOINT_ID;

        if (!RUNPOD_API_KEY || !RUNPOD_ENDPOINT_ID) {
            console.warn('RunPod config missing, returning mock success for local testing');
            // Mock delay
            await new Promise(resolve => setTimeout(resolve, 2000));
            return res.json({
                success: true,
                url: 'https://via.placeholder.com/1024x1024.png?text=Z-Image-Turbo+Remote+Render'
            });
        }

        const response = await axios.post(
            `https://api.runpod.ai/v2/${RUNPOD_ENDPOINT_ID}/runsync`,
            {
                input: {
                    prompt: prompt,
                    num_inference_steps: 9,
                    guidance_scale: 0.0,
                    width: 1024,
                    height: 1024,
                    safety_checker: false
                }
            },
            {
                headers: {
                    'Authorization': `Bearer ${RUNPOD_API_KEY}`,
                    'Content-Type': 'application/json'
                }
            }
        );

        res.json({ success: true, url: response.data.output });
    } catch (error) {
        console.error('RunPod Error:', error.message);
        res.status(500).json({ error: 'Failed to generate image on RunPod' });
    }
});

app.get('/api/balance', async (req, res) => {
    try {
        const RUNPOD_API_KEY = process.env.RUNPOD_API_KEY;
        if (!RUNPOD_API_KEY) return res.json({ balance: 'N/A' });

        const gqlResponse = await axios.post(
            'https://api.runpod.io/graphql',
            { query: 'query { myself { clientBalance } }' },
            {
                headers: {
                    'Authorization': `Bearer ${RUNPOD_API_KEY}`,
                    'Content-Type': 'application/json'
                }
            }
        );

        const balance = gqlResponse.data?.data?.myself?.clientBalance;
        res.json({ balance: balance ? `$${balance.toFixed(2)}` : 'ACTIVE' });
    } catch (error) {
        res.json({ balance: 'ACTIVE' });
    }
});

app.get('/api/model-test-results', async (req, res) => {
    try {
        const fs = require('fs');
        const path = require('path');
        
        // Try to load from backend directory
        const resultsPath = path.join(__dirname, '../backend/model_test_results.json');
        
        if (fs.existsSync(resultsPath)) {
            const results = JSON.parse(fs.readFileSync(resultsPath, 'utf8'));
            res.json(results);
        } else {
            // Return empty results if file doesn't exist
            res.json({ tested_at: null, results: [] });
        }
    } catch (error) {
        console.error('Error loading test results:', error);
        res.json({ tested_at: null, results: [], error: error.message });
    }
});

app.get('/api/model-test-results', async (req, res) => {
    try {
        const fs = require('fs');
        const path = require('path');
        
        // Try to load from backend directory
        const resultsPath = path.join(__dirname, '../backend/model_test_results.json');
        
        if (fs.existsSync(resultsPath)) {
            const results = JSON.parse(fs.readFileSync(resultsPath, 'utf8'));
            res.json(results);
        } else {
            // Return empty results if file doesn't exist
            res.json({ tested_at: null, results: [] });
        }
    } catch (error) {
        console.error('Error loading test results:', error);
        res.json({ tested_at: null, results: [], error: error.message });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
