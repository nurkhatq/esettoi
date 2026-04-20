import { NextResponse } from 'next/server';
import { Client } from 'pg';

const TELEGRAM_BOT_TOKEN = '8640737932:AAHsLpRu-PD3epqcA3-tqI8YaRaoSrba720';
const TELEGRAM_CHAT_IDS = ['1077964079', '1557952786'];

export async function POST(request) {
    try {
        const body = await request.json();
        const { name, status, wishes } = body;
        
        if (!name || !status) {
            return NextResponse.json({ error: 'Name and status are required' }, { status: 400 });
        }

        const cleanWishes = wishes ? wishes.trim() : '';

        // 1. Send to Telegram with 3 SECOND TIMEOUT
        let message = `🔔 **Жаңа жауап (60 жас):**\n\n👤 Аты-жөні: ${name}\n❓ Статусы: ${status}`;
        if (cleanWishes) {
            message += `\n💬 Тілегі: ${cleanWishes}`;
        }
        
        const telegramUrl = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
        for (const chatId of TELEGRAM_CHAT_IDS) {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 3000); 
                await fetch(telegramUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chat_id: chatId, text: message }),
                    signal: controller.signal
                }).catch(e => console.error("Telegram fail:", e.message));
                clearTimeout(timeoutId);
            } catch (err) {}
        }

        // 2. Save to Postgres
        const client = new Client({
            connectionString: process.env.DATABASE_URL
        });
        await client.connect();
        const result = await client.query(
            'INSERT INTO guests (name, status, wishes) VALUES ($1, $2, $3) RETURNING id',
            [name, status, cleanWishes]
        );
        await client.end();

        return NextResponse.json({ success: true, id: result.rows[0].id });
    } catch (err) {
        console.error("RSVP Error:", err);
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
