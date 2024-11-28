import React from 'react';
import { ProfileFormProps } from '../types';
import { Button } from './Button';
import styles from '../AdminProfile.module.css';

export const ProfileForm: React.FC<ProfileFormProps> = ({ onSubmit, initialData }) => {
  return (
    <form className={styles.profileForm} onSubmit={(e) => {
      e.preventDefault();
      onSubmit(initialData || { username: '', contactNo: '', emailAddress: '' });
    }}>
      <div className={styles.formGroup}>
        <label htmlFor="username" className={styles.formLabel}>Username</label>
        <input 
          id="username"
          type="text"
          className={styles.formInput}
          defaultValue={initialData?.username}
        />
      </div>
      
      <div className={styles.formGroup}>
        <label htmlFor="contactNo" className={styles.formLabel}>Contact No.</label>
        <input 
          id="contactNo"
          type="tel"
          className={styles.formInput}
          defaultValue={initialData?.contactNo}
        />
      </div>
      
      <div className={styles.formGroup}>
        <label htmlFor="emailAddress" className={styles.formLabel}>Email Address</label>
        <input 
          id="emailAddress"
          type="email"
          className={styles.formInput}
          defaultValue={initialData?.emailAddress}
        />
      </div>
      
      <div className={styles.formActions}>
        <Button variant="primary">Save</Button>
        <Button variant="secondary">Cancel</Button>
      </div>
    </form>
  );
};