import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

const getCsvPath = () => {
    return path.join(process.cwd(), 'data.csv');
};

export const dynamic = 'force-dynamic';

export async function GET() {
    try {
        const csvPath = getCsvPath();
        if (!fs.existsSync(csvPath)) {
            return NextResponse.json({ entries: [] });
        }

        const content = fs.readFileSync(csvPath, 'utf-8');
        const lines = content.split('\n').filter(line => line.trim().length > 0);
        
        const entries = [];
        // Skip header at index 0
        for (let i = 1; i < lines.length; i++) {
            // Very naive CSV parsing to handle the basic format we create
            // Format: "id","timestamp","name","status"
            const matches = lines[i].match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g);
            if (matches && matches.length >= 4) {
                entries.push({
                    id: matches[0].replace(/^"|"$/g, ''),
                    timestamp: matches[1].replace(/^"|"$/g, ''),
                    name: matches[2].replace(/^"|"$/g, '').replace(/""/g, '"'),
                    status: matches[3].replace(/^"|"$/g, '')
                });
            }
        }
        
        // Sort newest first
        entries.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

        return NextResponse.json({ entries });
    } catch (err) {
        console.error("Admin Fetch Error:", err);
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
