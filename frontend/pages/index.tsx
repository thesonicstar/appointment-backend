import SlotList from '@/components/SlotList';

export default function Home() {
  return (
    <div className="container">
      <h1>Appointment Booking</h1>
      <SlotList />
    </div>
  );
}
// This file is part of the frontend of an appointment booking application
// It imports the SlotList component which fetches and displays available appointment slots
// The Home component serves as the main entry point of the application
// It renders a welcome message and the list of available slots for users to book appointments.
// The SlotList component handles fetching the data from an API and displaying it to the user.
// The Home component is the main page of the application
// It serves as a landing page where users can see a welcome message
// and are prompted to log in to book an appointment slot.
// The Home component is the main entry point of the application
// It renders a welcome message and the list of available slots for users to book appointments.
// The SlotList component handles fetching the data from an API and displaying it to the user.

// This is the main page of the application
// It serves as a landing page where users can see a welcome message
// and are prompted to log in to book an appointment slot.