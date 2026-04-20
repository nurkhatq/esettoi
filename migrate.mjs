import { Client } from 'pg';

const client = new Client({
  connectionString: 'postgresql://neondb_owner:npg_hwou9WalvNp0@ep-royal-art-amtsjtjr-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require',
});

async function runMigration() {
  try {
    await client.connect();
    console.log('Connected to PG');
    
    await client.query(`
      CREATE TABLE IF NOT EXISTS guests (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        status VARCHAR(50) NOT NULL,
        wishes TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    console.log('Table "guests" created successfully!');
  } catch (err) {
    console.error('Migration failed:', err);
  } finally {
    await client.end();
  }
}

runMigration();
