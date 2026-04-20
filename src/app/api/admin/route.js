import { NextResponse } from 'next/server';
import { Client } from 'pg';

export async function GET() {
    try {
        const client = new Client({
            connectionString: process.env.DATABASE_URL
        });
        await client.connect();
        const result = await client.query('SELECT * FROM guests ORDER BY created_at DESC');
        await client.end();
        
        return NextResponse.json({ entries: result.rows });
    } catch (error) {
        console.error('Error reading DB:', error);
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
