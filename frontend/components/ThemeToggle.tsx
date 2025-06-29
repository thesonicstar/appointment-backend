import { useTheme } from '../context/ThemeContext';
import styles from './ThemeToggle.module.css';
import { Sun, Moon } from 'lucide-react'; // Optional icons from lucide-react

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className={styles.toggleWrapper}>
      <button className={styles.toggleButton} onClick={toggleTheme}>
        {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
      </button>
    </div>
  );
}

// This component toggles the theme between light and dark modes.
// It uses the `useTheme` hook from the context to access the current theme and the `toggleTheme` function.