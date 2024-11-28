import React from 'react';
import { HeaderProps } from './types';
import styles from './AdminDashboard.module.css';

export const Header: React.FC<HeaderProps> = ({ adminName, adminEmail, profileImage }) => {
  return (
    <div className={styles.headerContainer}>
      <img loading="lazy" src={profileImage} alt={`${adminName}'s profile`} className={styles.profileImage} />
      <div className={styles.adminName}>{adminName}</div>
      <div className={styles.adminEmail}>{adminEmail}</div>
    </div>
  );
};