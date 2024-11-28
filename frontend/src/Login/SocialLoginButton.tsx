import styles from './LoginForm.module.css';
import { SocialLoginButtonProps } from './types';

export const SocialLoginButton: React.FC<SocialLoginButtonProps> = ({ icon, text, variant, onClick }) => {
  const buttonClass = variant === 'primary' 
    ? styles.socialButtonPrimary 
    : variant === 'dark' 
      ? styles.socialButtonDark 
      : styles.socialButtonSecondary;

  const handleGoogleLogin = () => {
    window.location.href = 'http://127.0.0.1:8000/accounts/google/login/';
  };

  return (
    <button className={buttonClass} onClick={onClick || handleGoogleLogin}>
      <img loading="lazy" src={icon} alt="" className={styles.socialIcon} />
      <span className={styles.socialText}>{text}</span>
    </button>
  );
};
