import React from 'react';
import { PaginationProps } from './types';
import styles from './AdminDashboard.module.css';

export const Pagination: React.FC<PaginationProps> = ({ onPrevious, onNext }) => {
  return (
    <div className={styles.pagination}>
      <button onClick={onPrevious} className={styles.paginationButton}>Previous</button>
      <button onClick={onNext} className={styles.paginationButton}>Next</button>
    </div>
  );
};