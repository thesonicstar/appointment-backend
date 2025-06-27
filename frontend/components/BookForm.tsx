// components/BookForm.tsx
import { useState } from "react";

interface Slot {
  slot_id: string;
  datetime: string;
  doctor_id: string;
}

interface BookFormProps {
  slot: Slot;
  onSuccess: () => void;
}

export default function BookForm({ slot, onSuccess }: BookFormProps) {
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleBook = async () => {
    setLoading(true);
    setError("");

    const response = await fetch("https://7x307khvxf.execute-api.eu-west-2.amazonaws.com/Prod/book", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        slot_id: slot.slot_id,
        patient_id: "guest-user", // or a placeholder
        contact_email: email,
        contact_phone: phone,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      onSuccess();
    } else {
      setError(data.error || "Booking failed");
    }

    setLoading(false);
  };

  return (
    <div style={{ border: "1px solid #ccc", padding: 12, marginTop: 10 }}>
      <h3>Book Slot: {slot.datetime}</h3>
      <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <br />
      <input placeholder="Phone" value={phone} onChange={e => setPhone(e.target.value)} />
      <br />
      <button onClick={handleBook} disabled={loading}>
        {loading ? "Booking..." : "Book Appointment"}
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
