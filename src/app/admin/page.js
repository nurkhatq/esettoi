"use client";

import { useEffect, useState } from "react";

export default function AdminDashboard() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchEntries = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/admin");
      const data = await res.json();
      if (data.entries) {
        setEntries(data.entries);
      }
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchEntries();
  }, []);

  const handleDelete = async (id) => {
    if (!confirm("Дәл өшіресіз бе?")) return;
    try {
      const res = await fetch("/api/admin/delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id }),
      });
      if (res.ok) {
        fetchEntries();
      }
    } catch (err) {
      console.error(err);
      alert("Қате шықты");
    }
  };

  return (
    <div style={{ padding: "40px", maxWidth: "1000px", margin: "0 auto", fontFamily: "sans-serif" }}>
      <h1 style={{ fontSize: "24px", marginBottom: "20px" }}>Қонақтар тізімі (Админка)</h1>
      
      <div style={{ background: "#fff3cd", padding: "15px", borderRadius: "8px", marginBottom: "20px", border: "1px solid #ffeeba", color: "#856404" }}>
        <strong>Назар аударыңыз (Vercel):</strong> Бұл жазбалар уақытша файлда (data.csv) сақталады. Vercel сервері ұйықтағанда бұл файл өшіп қалуы мүмкін. Тізім Телеграмға міндетті түрде түсіп отырады!
      </div>

      {loading ? (
        <p>Жүктелуде...</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse", background: "#fff", boxShadow: "0 4px 6px rgba(0,0,0,0.1)" }}>
          <thead>
            <tr style={{ background: "#f8f9fa", borderBottom: "2px solid #dee2e6" }}>
              <th style={{ padding: "12px", textAlign: "left" }}>Уақыт</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Аты-жөні</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Статусы</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Тілегі</th>
              <th style={{ padding: "12px", textAlign: "center" }}>Әрекет</th>
            </tr>
          </thead>
          <tbody>
            {entries.length === 0 ? (
              <tr><td colSpan="5" style={{ padding: "12px", textAlign: "center" }}>Тізім бос</td></tr>
            ) : entries.map((entry) => (
              <tr key={entry.id} style={{ borderBottom: "1px solid #e9ecef" }}>
                <td style={{ padding: "12px", fontSize: "14px", color: "#666" }}>{new Date(entry.timestamp).toLocaleString("ru-RU")}</td>
                <td style={{ padding: "12px", fontWeight: "bold" }}>{entry.name}</td>
                <td style={{ padding: "12px" }}>
                  <span style={{ 
                    padding: "4px 8px", 
                    borderRadius: "4px", 
                    fontSize: "14px",
                    background: entry.status === "Келемін" ? "#d4edda" : "#f8d7da",
                    color: entry.status === "Келемін" ? "#155724" : "#721c24"
                  }}>
                    {entry.status}
                  </span>
                </td>
                <td style={{ padding: "12px", color: "#555", fontStyle: "italic", maxWidth: "250px" }}>{entry.wishes || "-"}</td>
                <td style={{ padding: "12px", textAlign: "center" }}>
                  <button 
                    onClick={() => handleDelete(entry.id)}
                    style={{ background: "#dc3545", color: "white", border: "none", padding: "6px 12px", borderRadius: "4px", cursor: "pointer" }}
                  >
                    Өшіру
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
