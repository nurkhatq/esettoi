import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

// Telegram Bot details
const TELEGRAM_BOT_TOKEN = '8640737932:AAHsLpRu-PD3epqcA3-tqI8YaRaoSrba720';
const TELEGRAM_CHAT_ID = '1077964079';

const getCsvPath = () => {
    return path.join(process.cwd(), 'data.csv');
};

export async function POST(request) {
    try {
        const body = await request.json();
        const { name, status, wishes } = body;
        
        if (!name || !status) {
            return NextResponse.json({ error: 'Name and status are required' }, { status: 400 });
        }

        const timestamp = new Date().toISOString();
        const entryId = Date.now().toString();
        const cleanWishes = wishes ? wishes.trim() : '';

        // 1. Send to Telegram with 3 SECOND TIMEOUT so it doesn't hang the CSV append!
        let message = `🔔 **Жаңа жауап (60 жас):**\n\n👤 Аты-жөні: ${name}\n❓ Статусы: ${status}`;
        if (cleanWishes) {
            message += `\n💬 Тілегі: ${cleanWishes}`;
        }
        
        const telegramUrl = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
        
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 3000); // 3 sec timeout

            await fetch(telegramUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    chat_id: TELEGRAM_CHAT_ID,
                    text: message,
                }),
                signal: controller.signal
            }).catch(e => console.error("Fetch promise error:", e.message));

            clearTimeout(timeoutId);
        } catch (botErr) {
            console.error("Telegram catch error:", botErr.message);
        }

        // 2. Save to CSV locally regardless of Telegram success
        const csvPath = getCsvPath();
        const safeName = name.replace(/"/g, '""');
        const safeWishes = cleanWishes.replace(/"/g, '""').replace(/\n/g, ' ');
        const csvLine = `"${entryId}","${timestamp}","${safeName}","${status}","${safeWishes}"\n`;
        
        if (!fs.existsSync(csvPath)) {
            // Create headers if doesn't exist
            fs.writeFileSync(csvPath, '"id","timestamp","name","status","wishes"\n');
        }
        fs.appendFileSync(csvPath, csvLine);

        return NextResponse.json({ success: true, id: entryId });
    } catch (err) {
        console.error("RSVP Error:", err);
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
