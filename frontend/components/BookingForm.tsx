import { useEffect, useState } from 'react';
import styles from './BookingForm.module.css';
import ThemeToggle from '../components/ThemeToggle';
import { useRouter } from 'next/router';


interface BookingFormProps {
  prefilledSlotId?: string;
}

export default function BookingForm({ prefilledSlotId }: BookingFormProps) {
  const [formData, setFormData] = useState({
    slotId: '',
    patientId: '',
    email: '',
    phone: ''
  });
  const router = useRouter();

  useEffect(() => {
    if (prefilledSlotId) {
      setFormData((prev) => ({ ...prev, slotId: prefilledSlotId }));
    }
  }, [prefilledSlotId]);

  const [modalMessage, setModalMessage] = useState('');
  const [isModalVisible, setModalVisible] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const res = await fetch('https://7x307khvxf.execute-api.eu-west-2.amazonaws.com/Prod/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          slot_id: formData.slotId,
          patient_id: formData.patientId,
          contact_email: formData.email,
          contact_phone: formData.phone
        })
      });

      if (!res.ok) throw new Error('Booking failed. Please try again.');

      const result = await res.json();
      setModalMessage(`✅ Booking successful! Appointment ID: ${result.appointment_id}`);
      // Reset the form
      setFormData({
        slotId: prefilledSlotId || '',
        patientId: '',
        email: '',
        phone: ''
      });
    } catch (err: any) {
      setModalMessage(`❌ ${err.message || 'An error occurred.'}`);
    } finally {
      setModalVisible(true);
    }
  };

  const closeModal = () => {
    setModalVisible(false);
  };

  return (
    <>
      <form className={styles.bookingForm} onSubmit={handleSubmit}>
        <ThemeToggle />
        <h2>Book an Appointment</h2>

        <label htmlFor="slotId">Slot ID*</label>
        <input type="text" id="slotId" name="slotId" value={formData.slotId} onChange={handleChange} required />

        <label htmlFor="patientId">Patient ID*</label>
        <input type="text" id="patientId" name="patientId" value={formData.patientId} onChange={handleChange} required />

        <label htmlFor="email">Email*</label>
        <input type="email" id="email" name="email" value={formData.email} onChange={handleChange} required />

        <label htmlFor="phone">Phone</label>
        <input type="tel" id="phone" name="phone" value={formData.phone} onChange={handleChange} />

        <button type="submit">Book Now</button>
          <button
            type="button"
            className={styles.backButton}
            onClick={() => router.push('/')}
          >
            ← Back to Home
          </button>
      </form>

      {isModalVisible && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal}>
            <p>{modalMessage}</p>
            <button onClick={closeModal}>Close</button>
          </div>
        </div>
      )}
    </>
  );
}
