import React from 'react';
import { MemberRowProps } from './types';
import styles from './MemberDashboard.module.css';

export const MemberRow: React.FC<MemberRowProps> = ({ name, memberId, dateEnrolled, dateExpiration }) => {
  return (
    <div className={styles.memberRow}>
      <div className={styles.memberName}>{name}</div>
      <div className={styles.memberDetails}>
        <div>{memberId}</div>
        <div>{dateEnrolled}</div>
      </div>
      <div className={styles.memberActions}>
        <div className={styles.expirationDate}>{dateExpiration}</div>
        <button className={styles.editButton}>Edit</button>
      </div>
    </div>
  );
};