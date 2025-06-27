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
  const [selectedSlot, setSelectedSlot] = useState<Slot | null>(null);
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [bookingError, setBookingError] = useState('');
  const [bookingSuccess, setBookingSuccess] = useState('');

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

  const handleBooking = async () => {
    if (!selectedSlot) return;

    try {
      const res = await fetch('https://7x307khvxf.execute-api.eu-west-2.amazonaws.com/Prod/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          slot_id: selectedSlot.slot_id,
          patient_id: 'guest-user', // hardcoded for now
          contact_email: email,
          contact_phone: phone,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Booking failed');

      setBookingSuccess('Appointment booked successfully!');
      setSelectedSlot(null);
      setEmail('');
      setPhone('');
    } catch (err: any) {
      setBookingError(err.message || 'Booking error');
    }
  };

  if (loading) return <p>Loading available slots...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>Available Slots</h2>
      <ul>
        {slots.map((slot) => (
          <li key={slot.slot_id}>
            <strong>{slot.datetime}</strong> with Dr. {slot.doctor_id}{' '}
            <button onClick={() => {
              setSelectedSlot(slot);
              setBookingSuccess('');
              setBookingError('');
            }}>
              Book
            </button>
          </li>
        ))}
      </ul>

      {selectedSlot && (
        <div style={{ marginTop: '1rem', padding: '1rem', border: '1px solid #ccc' }}>
          <h3>Booking for {selectedSlot.datetime}</h3>
          <input
            type="email"
            placeholder="Your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ display: 'block', marginBottom: '0.5rem' }}
          />
          <input
            type="tel"
            placeholder="Your phone"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            style={{ display: 'block', marginBottom: '0.5rem' }}
          />
          <button onClick={handleBooking}>Confirm Booking</button>
          <button onClick={() => setSelectedSlot(null)} style={{ marginLeft: '0.5rem' }}>
            Cancel
          </button>

          {bookingError && <p style={{ color: 'red' }}>{bookingError}</p>}
          {bookingSuccess && <p style={{ color: 'green' }}>{bookingSuccess}</p>}
        </div>
      )}
    </div>
  );
}
