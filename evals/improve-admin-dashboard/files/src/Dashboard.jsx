export default function Dashboard({ stats }) {
  return (
    <div style={{ fontFamily: "Inter, sans-serif", background: "linear-gradient(135deg,#7c3aed,#2563eb)", minHeight: "100vh", padding: 32 }}>
      <h1 style={{ color: "white" }}>✨ Welcome back, Admin!</h1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 24 }}>
        {stats.map((s) => (
          <div key={s.label} style={{ background: "white", borderRadius: 16, boxShadow: "0 10px 30px rgba(0,0,0,.2)", padding: 24 }}>
            <div style={{ fontSize: 48, fontWeight: 800 }}>{s.value}</div>
            <div>{s.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
