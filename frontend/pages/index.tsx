import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import styles from '../styles/Home.module.css';
import ThemeToggle from '../components/ThemeToggle';
import BookedSlotsList from '@/components/BookedSlotsList';

interface Slot {
  slot_id: string;
  datetime: string;
  doctor_id: string;
  available: boolean;
}

export default function Home() {
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
        setError(err.message || 'Error fetching slots');
      } finally {
        setLoading(false);
      }
    }

    fetchSlots();
  }, []);

  const handleSelectSlot = (slotId: string) => {
    router.push(`/book?slotId=${slotId}`);
  };

  return (
    <main className={styles.container}>
      <ThemeToggle />
      <h1>Book a Healthcare Appointment</h1>

      <section>
        <h2>Available Slots</h2>
        {loading && <p>Loading available slots...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}

        <ul className={styles.slotList}>
          {slots.map((slot) => (
            <li key={slot.slot_id} className={styles.slotCard}>
              <div className={styles.slotInfo}>
                <strong>{new Date(slot.datetime).toLocaleString()}</strong>
                <span>Doctor: {slot.doctor_id}</span>
                <span>Slot ID: {slot.slot_id}</span>
              </div>
              <button className={styles.bookButton} onClick={() => handleSelectSlot(slot.slot_id)}>
                Book
              </button>
            </li>
          ))}
        </ul>
      </section>

      <section style={{ marginTop: '2rem' }}>
        <BookedSlotsList />
      </section>
    </main>
  );
}
