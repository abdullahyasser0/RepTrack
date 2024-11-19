import styles from './LoginForm.module.css';  // Import the styles as an object
import { InputFieldProps } from './types';

export const InputField: React.FC<InputFieldProps> = ({ label, type = "text", value, icon, onChange }) => {
  return (
    <div className={styles.inputContainer}>
      <label className={styles.inputLabel}>{label}</label>
      <div className={styles.inputWrapper}>
        <input
          type={type}
          value={value}
          onChange={onChange}
          className={styles.inputField}
          aria-label={label}
        />
        {icon && <img loading="lazy" src={icon} alt="" className={styles.inputIcon} />}
      </div>
    </div>
  );
};