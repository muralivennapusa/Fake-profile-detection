import instaloader
import csv

#	fake	profile_pic	ratio_numlen_username	len_fullname	ratio_numlen_fullname	sim_name_username	len_desc	extern_url	private	num_posts	num_followers	num_following

csvfilename = "testdata0.csv"

data = [
    ['User-Name', 'Has-Profile-Pic', 'Number-of-Posts','User-Name-Length', 'Full-Name','Full-Name-Length', 'Follower-Count', 'Following-Count','Is-Private','BIO']
]
testdata=[
    ['','fake','profile_pic','ratio_numlen_username','len_fullname','ratio_numlen_fullname','sim_name_username','len_desc','extern_url','private','num_posts','num_followers','num_following','username','full_name']
]

def read_file(filename):
    words = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                word = line.strip()  # Remove leading/trailing whitespace
                if word:  # Check if the line is not empty after stripping
                    words.append(word)
        return words
    except FileNotFoundError:
        print("File not found.")
        return []

c=0

def get_instagram_profile_info():
    # Create an instance of Instaloader
    L = instaloader.Instaloader()
    try:
        L.context.login("siriussnyder", "blackCut")
    except instaloader.exceptions.ConnectionException as e:
        print(f"Login Error:{e}")
    except instaloader.exceptions.BadCredentialsException:
        print("Invalid username or password. Please double-check your credentials.")
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        filename = "users0.txt"  # Change this to the path of your .txt file
        usernames= read_file(filename)

        for username in usernames:
            global c
            a=[]            
            a.append(c)
            c=c+1
            a.append('')

            # Load the profile of the specified username
            profile = instaloader.Profile.from_username(L.context, username)

            # Check if the profile has a profile picture5
            has_profile_pic = profile.profile_pic_url != None
            a.append("Yes" if has_profile_pic else "No")  

            # number to username ratio for username
            ratio_username_numbers=len([1 for i in username if i.isdigit()])/len(username)
            a.append(ratio_username_numbers)

            # Get the full name length
            full_name = profile.full_name
            a.append(len(full_name))    

            try:
                #fullname number to name ratio 
                ratio_fullname_numbers=len([1 for i in full_name if i.isdigit()])/len(full_name)
                a.append(ratio_fullname_numbers)
            except Exception:
                a.append("0")
            else:
                a.append("0")
            #username to full name match
            if username == full_name:
                a.append("Full match")
            elif username in full_name or full_name in username:
                a.append("Partial match")
            else:
                a.append("No match")

            # Get the bio
            bio = profile.biography
            try:
                bio.encode(encoding='utf-8').decode('ascii')
            except UnicodeDecodeError:
                a.append("Invalid bio encoding")
            else:
                a.append(len(bio))

            #External URL
            try:
                if "Http" in bio:
                    a.append("Yes")
            except UnicodeDecodeError:
                a.append("Invalid bio encoding")
            else:
                a.append("No")
                
            # Check if the account is private
            is_private = profile.is_private
            a.append("Yes" if is_private else "No")

            # Get the number of posts
            num_posts = profile.mediacount
            a.append(num_posts)
            
            # Get the total number of followers
            num_followers = profile.followers
            a.append(num_followers)
            
            # Get the total number following
            num_following = profile.followees
            a.append(num_following)
            
            # Get the length of the username
            username_length = len(username)
            a.append(username)
            
            # Get the length of the full name
            full_name_length = len(profile.full_name)
            a.append(full_name)
            
            
            
            # Print the gathered information
            print("Username:", username)
            print("Profile Picture:", "Yes" if has_profile_pic else "No")
            print("Number of Posts:", num_posts)
            print("Length of Username:", username_length)
            print("Length of Full Name:", full_name_length)
            print("Full Name:", full_name)
            print("Words in Full Name:", len(full_name.split()))
            print("Total Followers:", num_followers)
            print("Total Following:", num_following)
            print("Account is Private:", is_private)
            print("Bio:", bio)
            print("________________________________________________________________")
            testdata.append(a)

    except instaloader.exceptions.ProfileNotExistsException:
        print("Profile not found for the given username.")
    global csvfilename
    write_to_csv(csvfilename, testdata)


def write_to_csv(filename, testdata):
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in testdata:
                try:    
                    writer.writerow(row)
                except Exception as e:
                    continue
        print(f"Data has been successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

get_instagram_profile_info()
write_to_csv(csvfilename, testdata)
