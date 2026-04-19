import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

const getCsvPath = () => {
    return path.join(process.cwd(), 'data.csv');
};

export async function POST(request) {
    try {
        const body = await request.json();
        const { id } = body;
        
        if (!id) {
            return NextResponse.json({ error: 'ID is required' }, { status: 400 });
        }

        const csvPath = getCsvPath();
        if (!fs.existsSync(csvPath)) {
            return NextResponse.json({ error: 'File not found' }, { status: 404 });
        }

        const content = fs.readFileSync(csvPath, 'utf-8');
        const lines = content.split('\n').filter(line => line.trim().length > 0);
        
        const newLines = lines.filter((line, index) => {
            if (index === 0) return true; // keep header
            const matches = line.match(/(?:^|,)("(?:[^"]|"")*"|[^,]*)/);
            if (matches && matches[1]) {
                const rowId = matches[1].replace(/^"|"$/g, '');
                return rowId !== id;
            }
            return true;
        });

        fs.writeFileSync(csvPath, newLines.join('\n') + '\n');

        return NextResponse.json({ success: true });
    } catch (err) {
        console.error("Admin Delete Error:", err);
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
