import { useEffect, useState } from 'react';

interface Slot {
  slot_id: string;
  datetime: string;
  doctor_id: string;
  available: boolean;
}

export default function SlotList() {
  const [slots, setSlots] = useState<Slot[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchSlots() {
      try {
        const res = await fetch('https://7x307khvxf.execute-api.eu-west-2.amazonaws.com/Prod/slots');
        if (!res.ok) throw new Error('Failed to fetch slots');
        const data = await res.json();
        setSlots(data);
      } catch (err: any) {
        console.error(err);
        setError(err.message || 'Error fetching slots');
      } finally {
        setLoading(false);
      }
    }

    fetchSlots();
  }, []);

  if (loading) return <p>Loading available slots...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>Available Slots</h2>
      <ul>
        {slots.map((slot) => (
          <li key={slot.slot_id}>
            <strong>{slot.datetime}</strong> with Dr. {slot.doctor_id}
          </li>
        ))}
      </ul>
    </div>
  );
}
// This component fetches and displays a list of available appointment slots
// It uses the useEffect hook to fetch data from an API endpoint 