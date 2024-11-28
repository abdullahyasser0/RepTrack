import React from 'react';
import { SidebarItem } from './components/Sidebarltem';
import { ProfileForm } from './components/ProfileForm';
import { Button } from './components/Button';
import styles from './AdminProfile.module.css';

const sidebarItems = [
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/e5b1e5633d6552fb186cda6d7b018a7309401bc6476ac546ea456b7a53218ee2?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Dashboard' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/2f8a5dd1d83d27a28e4eca35808457e7f8d0a8e37eaf511d7fc7a39d2318e10b?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Admin Profile', isActive: true },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/924cd441e1c0088fd992bf81e391ca48c62c1aed5c4175f8e7e0017d16337df3?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Registration' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/0886e95868ba85d5d6bdafaf72ed0793829d5702a804a69eaf1a41a264d5cdf6?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Plan' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/4b76805a4712990364cab8cf64a035e42a288ef37941ddcc4e6d175a140ea816?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Payment' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/31908d30b0e0a7420a7d52bb646f3e0ed49dd0ace7bd8d00a5168a9b292bfe78?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Inventory' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/69ff5cc2990ec855605c052db15517001ae42016cd0a58f8365f679f12e33d66?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'View Members' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/d95ce50284bc9a30712d0f65a6ab45bee539aee7a4c3af6597806b147c66c27a?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Coaches' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/f036a1fcc49c96f3e3303a62e30b3f8289c28f0ab9e16dca6d75d43358ca17ff?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Report' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/5abe64b7f65946c75260266d99dbfb0fcd82df1cbd1cd49329da6fe122dd8ce6?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Logout' }
];

export const AdminProfile: React.FC = () => {
  return (
    <div className={styles.adminProfilePage}>
      <div className={styles.container}>
        <aside className={styles.sidebar}>
          <div className={styles.profileHeader}>
            <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/e169edf2daeb05638a3e738ed4735d4045d9b66452da395960b715feaa8a6892?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9" alt="Administrator" className={styles.profileImage} />
            <h2 className={styles.profileName}>Administrator Name</h2>
            <p className={styles.profileEmail}>juan.delacruz@gmail.com</p>
          </div>
          
          <nav className={styles.sidebarNav}>
            {sidebarItems.map((item, index) => (
              <SidebarItem
                key={index}
                icon={item.icon}
                label={item.label}
                isActive={item.isActive}
              />
            ))}
          </nav>
        </aside>
        
        <main className={styles.mainContent}>
          <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/ea58de615482b6fbb8bdb9990c83b114973529133782fdc8e652424da510dbaf?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9" alt="" className={styles.decorativeImage} />
          
          <section className={styles.adminInfo}>
            <h1 className={styles.pageTitle}>Admin Information</h1>
            
            <div className={styles.contentGrid}>
              <div className={styles.profileCard}>
                <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/093c3067bc0b838a4028d73728184a6c616b5a46dae40a7348d085e0d295d682?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9" alt="Profile" className={styles.profileCardImage} />
                <div className={styles.updateProfile}>
                  <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/7b91e7210d0e54770cff9350631cec610c7995660752242ebdb7d620e33c20fb?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9" alt="" className={styles.updateIcon} />
                  <span>Update Profile</span>
                </div>
                
                <div className={styles.profileDetails}>
                  <div className={styles.detailRow}>
                    <span className={styles.detailLabel}>Username</span>
                    <span className={styles.detailValue}>JuanDelaCruz</span>
                  </div>
                  <div className={styles.detailRow}>
                    <span className={styles.detailLabel}>Contact no.</span>
                    <span className={styles.detailValue}>09123456789</span>
                  </div>
                  <div className={styles.detailRow}>
                    <span className={styles.detailLabel}>Email Address:</span>
                    <span className={styles.detailValue}>juan.delacruz@gmail.com</span>
                  </div>
                </div>
                
                <Button variant="primary">Register New Admin Account</Button>
              </div>
              
              <div className={styles.formSection}>
                <ProfileForm
                  onSubmit={(data) => console.log(data)}
                  initialData={{
                    username: 'JuanDelaCruz',
                    contactNo: '09123456789',
                    emailAddress: 'juan.delacruz@gmail.com'
                  }}
                />
                
                <div className={styles.passwordSection}>
                  <h3 className={styles.passwordTitle}>Password</h3>
                  <form className={styles.passwordForm}>
                    <div className={styles.formGroup}>
                      <label htmlFor="currentPassword" className={styles.formLabel}>
                        Current Password
                      </label>
                      <input
                        id="currentPassword"
                        type="password"
                        className={styles.formInput}
                      />
                    </div>
                    
                    <div className={styles.formGroup}>
                      <label htmlFor="newPassword" className={styles.formLabel}>
                        New Password
                      </label>
                      <input
                        id="newPassword"
                        type="password"
                        className={styles.formInput}
                      />
                    </div>
                    
                    <div className={styles.formGroup}>
                      <label htmlFor="retypePassword" className={styles.formLabel}>
                        Re-type Password
                      </label>
                      <input
                        id="retypePassword"
                        type="password"
                        className={styles.formInput}
                      />
                    </div>
                    
                    <div className={styles.formActions}>
                      <Button variant="primary">Change</Button>
                      <Button variant="secondary">Clear</Button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};