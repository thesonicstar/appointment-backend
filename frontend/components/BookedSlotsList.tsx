import { useEffect, useState } from 'react';
import styles from './BookedSlotsList.module.css';

interface Appointment {
  appointment_id: string;
  slot_id: string;
  doctor_id?: string;
  datetime?: string;
  status: string;
}

export default function BookedSlotsList() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [confirmingId, setConfirmingId] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState('');

  const patientId = 'pat-001'; // Replace with dynamic value when available

  useEffect(() => {
    async function fetchAppointments() {
      try {
        const res = await fetch(
          `https://7x307khvxf.execute-api.eu-west-2.amazonaws.com/Prod/my-appointments?patient_id=${patientId}`
        );
        if (!res.ok) throw new Error('Failed to fetch appointments');
        const data = await res.json();
        setAppointments(data);
      } catch (err: any) {
        setError(err.message || 'Error fetching appointments');
      } finally {
        setLoading(false);
      }
    }

    fetchAppointments();
  }, []);

  const handleCancel = async (appointmentId: string) => {
    try {
      const res = await fetch(
        `https://7x307khvxf.execute-api.eu-west-2.amazonaws.com/Prod/cancel`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ appointment_id: appointmentId })
        }
      );

      if (!res.ok) throw new Error('Cancellation failed');

      setSuccessMsg('Appointment cancelled successfully!');
      setAppointments((prev) =>
        prev.filter((app) => app.appointment_id !== appointmentId)
      );
    } catch (err: any) {
      alert(err.message || 'Cancellation failed');
    } finally {
      setConfirmingId(null);
    }
  };

  if (loading) return <p>Loading booked appointments...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div className={styles.container}>
      <h2>Your Booked Appointments</h2>
      {successMsg && <p className={styles.success}>{successMsg}</p>}
      <ul className={styles.appointmentList}>
        {appointments.map((app) => (
          <li key={app.appointment_id} className={styles.appointmentItem}>
            <div className={styles.details}>
              <strong>
                {app.datetime
                  ? new Date(app.datetime).toLocaleString()
                  : 'No date/time available'}
              </strong>
              <span>Doctor: {app.doctor_id || 'N/A'}</span>
              <span>Appointment ID: {app.appointment_id}</span>
              <span>Status: {app.status}</span>
            </div>
            <button
              className={styles.cancelButton}
              onClick={() => setConfirmingId(app.appointment_id)}
            >
              Cancel
            </button>

            {confirmingId === app.appointment_id && (
              <div className={styles.confirmBox}>
                <p>Are you sure you want to cancel?</p>
                <button
                  className={styles.confirmButton}
                  onClick={() => handleCancel(app.appointment_id)}
                >
                  Yes, Cancel
                </button>
                <button
                  className={styles.noButton}
                  onClick={() => setConfirmingId(null)}
                >
                  No
                </button>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
