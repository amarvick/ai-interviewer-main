import styles from "./FullPageSpinner.module.css";

interface FullPageSpinnerProps {
  label?: string;
}

export default function FullPageSpinner({ label = "Loading" }: FullPageSpinnerProps) {
  return (
    <div className={styles.backdrop} role="status" aria-live="polite" aria-busy="true">
      <div className={styles.spinner} />
      {label ? <span className={styles.label}>{label}</span> : null}
    </div>
  );
}
