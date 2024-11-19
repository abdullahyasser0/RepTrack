import React from 'react';
import styles from './SignupForm.module.css';
import { InputFieldProps } from './types';

export const InputField: React.FC<InputFieldProps> = ({ placeholder, type = 'text', icon }) => {
  return (
    <div className={styles.inputWrapper}>
      <input
        type={type}
        placeholder={placeholder}
        className={styles.inputField}
        aria-label={placeholder}
      />
      {icon && <img src={icon} alt="" className={styles.inputIcon} />}
    </div>
  );
};