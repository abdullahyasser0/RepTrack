import React from 'react';
import styles from './SignupForm.module.css';
import { SocialSignupButtonProps } from './types';

export const SocialSignupButton: React.FC<SocialSignupButtonProps> = ({ icon, text, variant, onClick }) => {
  const buttonClass = variant === 'facebook' 
    ? styles.socialButtonFacebook 
    : variant === 'google' 
      ? styles.socialButtonGoogle 
      : styles.socialButtonX;

  return (
    <button className={buttonClass} onClick={onClick}>
      <img src={icon} alt="" className={styles.socialIcon} />
      <span className={styles.socialButtonText}>{text}</span>
    </button>
  );
};