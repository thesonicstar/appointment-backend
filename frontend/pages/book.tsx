import { useRouter } from 'next/router';
import BookingForm from '../components/BookingForm';

export default function BookPage() {
  const router = useRouter();
  const { slotId } = router.query;

  return (
    <main>
      <h1>Book Your Appointment</h1>
      {typeof slotId === 'string' ? (
        <BookingForm prefilledSlotId={slotId} />
      ) : (
        <p>Loading...</p>
      )}
    </main>
  );
}
// This page component retrieves the slot ID from the URL query parameters and passes it to the BookingForm component.
// It ensures that the booking form is only rendered once the slot ID is available, providing a loading state in the meantime.
// The BookingForm component is responsible for handling the booking logic, including form submission and API interaction