import styles from './LoginForm.module.css';
import { SocialLoginButtonProps } from './types';

export const SocialLoginButton: React.FC<SocialLoginButtonProps> = ({ icon, text, variant, onClick }) => {
  const buttonClass = variant === 'primary' 
    ? styles.socialButtonPrimary 
    : variant === 'dark' 
      ? styles.socialButtonDark 
      : styles.socialButtonSecondary;

  return (
    <button className={buttonClass} onClick={onClick}>
      <img loading="lazy" src={icon} alt="" className={styles.socialIcon} />
      <span className={styles.socialText}>{text}</span>
    </button>
  );
};