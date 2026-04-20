import { NextResponse } from 'next/server';
import { Client } from 'pg';

export async function POST(request) {
    try {
        const body = await request.json();
        const { id } = body;
        
        if (!id) {
            return NextResponse.json({ error: 'ID required' }, { status: 400 });
        }

        const client = new Client({
            connectionString: process.env.DATABASE_URL
        });
        await client.connect();
        await client.query('DELETE FROM guests WHERE id = $1', [id]);
        await client.end();
        
        return NextResponse.json({ success: true });
    } catch (error) {
        console.error('Error deleting:', error);
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
