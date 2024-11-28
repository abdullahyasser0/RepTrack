import React from 'react';
import { ButtonProps } from '../types';
import styles from '../AdminProfile.module.css';

export const Button: React.FC<ButtonProps> = ({ variant, children, onClick }) => {
  const buttonClass = variant === 'primary' ? styles.buttonPrimary : styles.buttonSecondary;
  
  return (
    <button className={buttonClass} onClick={onClick}>
      {children}
    </button>
  );
};