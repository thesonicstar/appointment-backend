import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

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
  const router = useRouter();

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

  const handleBookClick = (slotId: string) => {
    router.push(`/book?slotId=${slotId}`);
  };

  if (loading) return <p>Loading available slots...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>Available Slots</h2>
      <ul>
        {slots.map((slot) => (
          <li key={slot.slot_id} style={{ marginBottom: '1rem' }}>
            <strong>{slot.datetime}</strong> with Dr. {slot.doctor_id}
            <br />
            <button onClick={() => handleBookClick(slot.slot_id)}>Book Now</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
// This component fetches available slots from the API and displays them in a list.
// Each slot has a "Book Now" button that navigates to the booking page with the slot ID as a query parameter.
// The component handles loading and error states, providing feedback to the user.