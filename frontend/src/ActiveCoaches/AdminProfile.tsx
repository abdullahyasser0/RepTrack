import React from 'react';
import { AdminProfileProps } from './types';
import styles from './MemberDashboard.module.css';

export const AdminProfile: React.FC<AdminProfileProps> = ({ name, email, avatar }) => {
  return (
    <div className={styles.adminProfile}>
      <img src={avatar} alt={`${name}'s profile`} className={styles.adminAvatar} />
      <div className={styles.adminName}>{name}</div>
      <div className={styles.adminEmail}>{email}</div>
    </div>
  );
};