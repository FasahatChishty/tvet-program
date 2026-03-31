from backend.backend_logic import (
    register_student,
    login_student,
    recover_student_id,
    recover_password,
    take_test,
    compute_scores,
    compute_tvet_index,
    recommend_domain,
    recommend_path,
    record_and_notify,
    test_email_config,
    send_results_to_all_users
)


def show_email_setup_menu():
    """Show menu for email configuration help."""
    print("\n" + "="*60)
    print("📧 EMAIL CONFIGURATION HELP")
    print("="*60)
    print("\n1. Configure Email Credentials")
    print("2. Test Email Configuration")
    print("3. View Configuration Instructions")
    print("4. Return to Main Menu")
    choice = input("\nChoice: ").strip()
    
    if choice == "1":
        print("\n" + "="*60)
        print("QUICK EMAIL SETUP (GMAIL)")
        print("="*60)
        print("\nSteps:")
        print("1. Go to https://myaccount.google.com/")
        print("2. Click Security → 2-Step Verification")
        print("3. Go to https://myaccount.google.com/apppasswords")
        print("4. Select Mail + Windows Computer")
        print("5. Copy the 16-character password")
        print("\nThen update backend/backend_logic.py lines 15-16:")
        print('  EMAIL_USER = os.environ.get("EMAIL_USER", "YOUR_EMAIL@gmail.com")')
        print('  EMAIL_PASS = os.environ.get("EMAIL_PASS", "YOUR-16-CHAR-PASSWORD")')
        input("\nPress Enter to continue...")
        
    elif choice == "2":
        test_email = input("\nEnter your email to test: ").strip()
        if "@" in test_email and "." in test_email:
            print("\nAttempting to send test email...")
            test_email_config(test_email)
        else:
            print("❌ Invalid email format")
            
    elif choice == "3":
        print("\nOpening EMAIL_CONFIG.txt instructions...")
        print("Please read EMAIL_CONFIG.txt in the project root directory.")
        input("Press Enter to continue...")
        
    return choice != "4"


def main():
    print("===== STUDENT ASSESSMENT SYSTEM =====")
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Recover Student ID")
        print("4. Recover Password")
        print("5. Email Configuration Help")
        print("6. Send Results to All Users")
        print("7. Exit")
        choice = input("Choose option: ").strip()

        if choice == "1":
            student_id, mode = register_student()
            print(f"Registered ID: {student_id} Mode: {mode}")
            # after registration automatically take test
            df, flags = take_test(student_id, mode)
            print("\n✅ Test Completed")
            
            # Display Anti-Cheating Results
            print("\n" + "="*50)
            print("🔒 ANTI-CHEATING ANALYSIS")
            print("="*50)
            print(f"Cheating Severity: {flags['cheating_severity']}")
            if flags['too_fast']:
                print("⚠️  WARNING: Test completed too quickly!")
            if flags['straight_lining']:
                print("⚠️  WARNING: Too many repeated answers detected!")
            print(f"Test Duration: {flags['total_duration_seconds']:.1f} seconds")
            print(f"Avg Time/Question: {flags['avg_time_per_question']:.1f} seconds")
            print(f"Repeated Answer Rate: {flags['repeat_answer_rate']*100:.1f}%")

            scores = compute_scores(df)
            print("\n" + "="*50)
            print("📊 DOMAIN SCORES")
            print("="*50)
            print(scores)

            index, label = compute_tvet_index(scores)
            print(f"\n📈 TVET Index: {index:.2f}")
            print(f"📌 Assessment Level: {label}")

            domain, all_scores = recommend_domain(scores)
            print(f"\n🎯 Recommended Technical Domain: {domain}")
            
            path_rec, path_exp, fyp_s, job_s = recommend_path(scores, mode)
            print(f"\n🚀 Recommended Path: {path_rec}")
            print(f"💡 {path_exp}")
            print(f"   FYP Aptitude: {fyp_s:.2f}/100")
            print(f"   JOB Aptitude: {job_s:.2f}/100")

            record_and_notify(student_id, scores, index, label, domain, mode)
           # Ask what to do next
            print("\n=== What would you like to do next? ===")
            print("1. Return to Main Menu")
            print("2. Exit")
            next_choice = input("Choose: ").strip()
            if next_choice == "2":
                print("Exiting...")
                break
            # else continue to main menu

        elif choice == "2":
            student_id, mode = login_student()
            if student_id:
                print(f"Logged in ID: {student_id} Mode: {mode}")

                # Take Test
                df, flags = take_test(student_id, mode)
                print("\n✅ Test Completed")
                
                # Display Anti-Cheating Results
                print("\n" + "="*50)
                print("🔒 ANTI-CHEATING ANALYSIS")
                print("="*50)
                print(f"Cheating Severity: {flags['cheating_severity']}")
                if flags['too_fast']:
                    print("⚠️  WARNING: Test completed too quickly!")
                if flags['straight_lining']:
                    print("⚠️  WARNING: Too many repeated answers detected!")
                print(f"Test Duration: {flags['total_duration_seconds']:.1f} seconds")
                print(f"Avg Time/Question: {flags['avg_time_per_question']:.1f} seconds")
                print(f"Repeated Answer Rate: {flags['repeat_answer_rate']*100:.1f}%")

                # Compute Scores
                scores = compute_scores(df)
                print("\n" + "="*50)
                print("📊 DOMAIN SCORES")
                print("="*50)
                print(scores)

                # TVET Index
                index, label = compute_tvet_index(scores)
                print(f"\n📈 TVET Index: {index:.2f}")
                print(f"📌 Assessment Level: {label}")

                # Recommended Domain
                domain, all_scores = recommend_domain(scores)
                print(f"\n🎯 Recommended Technical Domain: {domain}")
                
                path_rec, path_exp, fyp_s, job_s = recommend_path(scores, mode)
                print(f"\n🚀 Recommended Path: {path_rec}")
                print(f"💡 {path_exp}")
                print(f"   FYP Aptitude: {fyp_s:.2f}/100")
                print(f"   JOB Aptitude: {job_s:.2f}/100")

                # record summary and email
                record_and_notify(student_id, scores, index, label, domain, mode)

                # Ask what to do next
                print("\n=== What would you like to do next? ===")
                print("1. Return to Main Menu")
                print("2. Exit")
                next_choice = input("Choose: ").strip()
                if next_choice == "2":
                    print("Exiting...")
                    break
                # else continue to main menu

        elif choice == "3":
            recover_student_id()

        elif choice == "4":
            recover_password()

        elif choice == "5":
            show_email_setup_menu()

        elif choice == "6":
            send_results_to_all_users()

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()


