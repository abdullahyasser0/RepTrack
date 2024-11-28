import React from 'react';
import { CoachItemProps } from './types';
import styles from './AdminDashboard.module.css';

export const CoachItem: React.FC<CoachItemProps> = ({ name, id, contact, expirationDate }) => {
  return (
    <div className={styles.coachItem}>
      <div className={styles.coachInfo}>
        <div className={styles.coachName}>{name}</div>
        <div className={styles.coachId}>{id}</div>
      </div>
      <div className={styles.coachContact}>{contact}</div>
      <div className={styles.coachExpiration}>{expirationDate}</div>
      <button className={styles.editButton}>Edit</button>
    </div>
  );
};