import sqlite3
import sys
from datetime import date
import getpass



today = date.today()

def create_user():
    cr_success = 0
    #User enters a user ID, a name, password and city
    userID = input("Enter a userID: ")
    user_name = input("Enter your name: ")
    password = getpass.getpass(prompt = "Enter a password")
    city = input("Which city are you from? ")
    
    try:
        with conn:  
            c.execute('''
            INSERT INTO users (uid, name, pwd, city, crdate)
            VALUES (?, ?, ?, ?, ?);
            ''', (userID, user_name, password, city, today),
            )
            conn.commit()
            #Inserts the user ID, name, password and city into the database
            cr_success = 1
        
    except sqlite3.Error as e:
        cr_success = 0
        print(e)
        
    finally:
        if cr_success == 0:
            #If insertion is unsuccessful, the code returns to login menu without any insertion
            print("User creation failed, returning to login menu.")
            print("You can return here again by trying to sign up again.")
            return
        else:
            #If insertion is successful, the code returns to login menu
            print("User creation successful, returning to login/sign-up menu.")
            return        

def startdb():
    if len(sys.argv) != 2: #python name.py <db>
        return False
    db_name = sys.argv[1]
    global conn, c
    try:
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        return True

    except Exception as e:
        print("unable to start db")
        return False





def login_menu():
    success = startdb()
    if not success:
        print("Unable to start db")
        print("Usage: python3 mini_project.py <dbpath>")
        return


    print("Hi, welcome to the application.") 
    while True:
        #Asks the user if he/she would like to sign up
        print("You are at the login/sign_up menu.\nIf you would like to exit, please type quit within this menu.")
        print("Would you like to sign up? (y/n) \nSelecting n will take you to the login.")
        answer = input()
        answer = answer.upper()
        if answer == 'Y':
            #If the user says Y, then the program lets the user sign up
            create_user()
        elif answer == 'N':
            #If the user says N, the progam asks the user to login
            print("Taking you to the login screen...")
            login()
        elif answer == 'QUIT':
            #If the user says QUIT, the program stops
            print("Exiting. Have a good day!")
            break
        else:
            print("Invalid input, try again. ")

    if conn is not None:
        conn.close()
            
def login():
    #Program asks user to enter username and password    
    userID = input("Enter your userID: ")
    password = getpass.getpass(prompt = "Enter your password: ")
    login_success = 0
    try:
        with conn:
            #Searches for the username and the password within the database
            c.execute(
                'SELECT uid, pwd FROM users WHERE lower(uid) = lower(?) AND pwd = ?;',
                (userID, password),
                )
            conn.commit()
        if c.fetchone() is None:
            login_success = 0
        else:
            login_success = 1
    except sqlite3.Error as e:
        login_success = 0
        print(e)
    finally:
        #If login is successful
        if login_success == 1:
            print("Login successful, taking you to the main menu.")
            main_menu(userID)
        else:
            print("Login unsuccessful, returning to the login/sign-up menu.")
            return 
            

def main_menu(userID):
    while True:
        #Asks the user to pick between the 2 options
        print("Hello and welcome to the main menu. There are a few things that you can do")
        print("Inorder to go the desired function just enter the number besides each option.")
        print("1) Post a question\n")
        print("2) Search for posts\n ")
        print("Type in quit to logout and go back into the login/sign-up menu.")
        response = input()
        response = response.upper()
        #If the user picks option 1, goes to post a question
        if response == '1':
            post_question(userID)
        #If the user picks option 2, goes to search for post
        elif response == '2':
            search_post(userID)
        #If the user enters quit, the program goes back to login menu
        elif response == 'QUIT':
            return
        else:
            print("Invalid user input. Please enter a valid option.")
       


def post_question(username):
    #Asks the user to enter the title and body of the new question post
    print("You can post a question here. Just provide title and body")
    title = input("Enter a title: ")
    body  = input("Enter a body: ")
    insert_success = 0
    try:
        with conn:
            c.execute('''SELECT * FROM posts''')
            conn.commit()
            rows = c.fetchall()
            number_rows = (len(rows) + 1)
            #gives us a unique numbered ID as the previous numbers are < current number generated
            postID_number = number_rows + 1 
            new_postID = 'p' + str(postID_number)
            
            #Inserts the post into the post table
            c.execute('''
            INSERT INTO posts (pid, pdate, title, body, poster) 
            VALUES (?,?,?,?,?);
            ''', (new_postID,today,title,body,username),
            )
            conn.commit()
            
            #Inserts the question pid into the questions table
            c.execute('''
            INSERT INTO questions(pid, theaid)
            VALUES(?, NULL);
            ''',(new_postID,),
            )

            conn.commit()
            
            #Inserts the tag pid into the tags table
            c.execute('''
            INSERT INTO tags VALUES(?, NULL)''', (new_postID,) ,) 
            conn.commit()
            insert_success = 1
    
    except sqlite3.Error as e:
        print(e)
        insert_success = 0

    finally:
        print("Trying")
        if insert_success == 1:
            #If the insertion was successful, returns to main menu
            print("Question posted. Returning to the main menu.")
            return
        else:
            #If the insertion was unsuccessful, returns to main menu without any insertion
            print("Question has not been posted, returning to the main menu.")
            return



def post_action_answer(userID, questionID):
    #Asks the user to enter the a title and body for the selected post
    print("Hi, in order to post an answer for your selected question, we need some more info.")
    title = input("Enter a title for your answer: ")
    body = input("Enter the body for your answer: ")
    postID_number = 0
    answer_insertion_success = 0
    try:
        with conn:
            c.execute('''SELECT * FROM posts;''')
            conn.commit()
            rows = c.fetchall()
            number_rows = (len(rows) + 1)
        
        #gives us a unique numbered ID as the previous numbers are < current number generated
        postID_number = number_rows + 1 
        new_postID = 'p' + str(postID_number)
        with conn:
            #Inserts the post into the posts table
            c.execute('''
            INSERT INTO posts(pid, pdate, title, body, poster)
            VALUES(?, ?, ?, ?, ?);''', (new_postID, today, title, body, userID),
            )
            conn.commit()
            
            #Insert the answer post into the answers table 
            c.execute('''
            INSERT INTO answers(pid, qid)
            VALUES(?, ?);''', (new_postID, questionID),
            )
            conn.commit()
            
            #Inserts the tag into the tags table
            c.execute('''
            INSERT INTO tags VALUES(?, NULL);''', (new_postID,),)
            conn.commit()
            answer_insertion_success = 1
    
    except sqlite3.Error as e:
        print(e)
        answer_insertion_success = 0
    finally:
        #If the insertion was unsuccessful, returns to main menu without any insertion
        if answer_insertion_success == 0:
            print("Answer insertion failed, returning to the main menu.")
            return
        #If the insertion was successful, returns to main menu
        else:
            print("Answer insertion successful, returning to the main menu.")
            return




def post_action_vote(pid, userID):
    print("In order to be able to vote, we must check your eligibility")
    print("If you have voted on this post before you won't be able to vote again.")
    voting_success = 0
    vote_number = 0
    with conn:
        #Checks if the user has already voted in the selected post
        c.execute("SELECT * from votes where pid = ? and uid = ?;", (pid, userID),)
        conn.commit()
    if c.fetchone() is None:
        with conn:
            c.execute("SELECT * FROM votes;")
            conn.commit()
            rows = c.fetchall()
            vote_number = len(rows) + 1
            try:
                #Inserts vote into vote table
                c.execute("INSERT INTO votes VALUES (?, ?, ?, ?);", (pid, vote_number, today, userID), )
                conn.commit()
                voting_success = 1
            except sqlite3.Error as e:
                print(e)
                voting_success = 0
            finally:
                #If the voting was successful, returns to main menu
                if voting_success == 1:
                    print("Vote inserted successfully. Returning to the previous page.")
                    return
                #If the voting was unsuccessful, returns to main menu without any insertion
                else:
                    print("Vote insertion unsuccessful. Returning to the previous page.")
                    return
    #If the user has already voted on the selected post
    else:
        print("You have voted on this post before already. Returning to the previous page.")
        return
   




def post_action_accepted(pid):
    #Checks if the selected post already has an accepted answer
    print("Checking if there already is an accepted answer for the question you're answering.")
    update_success = 0
    with conn:
        c.execute("SELECT qid from answers where pid = ?;", (pid,))
        conn.commit()
        row = c.fetchone()
        qid = row[0]
        c.execute("SELECT COUNT(theaid) from questions where pid = ?;", (qid,), )
        conn.commit()
        row = c.fetchone()
        #If there are no accepted answer
        if row[0] == 0:
            print("There isn't currently an accepted answer.\nTrying to set your answer as the accepted answer.")
            try:
                #Updates the question table so that it has the answer as the accepted answer
                c.execute("UPDATE questions SET theaid = ? WHERE pid = ?;", (pid, qid), )
                conn.commit()
                update_success = 1
            except sqlite3.Error as e:
                print(e)
                update_success = 0
            finally:
                #If the update was unsuccessful, returns to main menu without any insertion
                if update_success == 0:
                    print("Unsuccessful at setting the answer as the accepted answer.")
                    print("Returning to the previous page.")
                    return
                #If the update was successful, returns to main menu
                else:
                    print("Update successful. Your selected answer is the new accepted answer.")
                    print("Returning to the previous page.")
        else:
            while True:
                #If there is already an accepted answer
                print("There already is an accepted answer for this question.\nWould you like to change it?")
                response = input("Enter Y/N: ")
                response = response.upper()
                #If user types y, then it picks selected answer as accepted answer
                if response == 'Y':
                    print("Okay trying to set your selected answer as the accepted answer.")
                    with conn:
                        try:
                            #Updates the questions table
                            c.execute("UPDATE questions SET theaid = ? WHERE pid = ?;", (pid, qid), )
                            conn.commit()
                            update_success = 1
                        except sqlite3.Error as e:
                            print(e)
                            update_success = 0
                        finally:
                            #If update was successful, returns to main menu
                            if update_success == 1:
                                print("Update successful. Your selected answer is the new accepted answer.")
                                print("Returning to the previous page.")
                                return
                            #If the update was unsuccessful, returns to main menu without any insertion
                            else:
                                print("Unsuccessful at setting the answer as the accepted answer.")
                                print("Returning to the previous page.")
                                return
                #If user enters n, it does not change question's accepted answer and returns to search post
                elif response == 'N':
                    print("Okay. Will not be changing the question's accepted answer.")
                    print("Returning to the previous page.")
                    return
                #If user enters anything other than y or n
                else:
                    print("Invalid input. Enter again.")






def post_action_give_badge(pid):
    invalid = 1
    while invalid == 1:
        with conn:
            c.execute("SELECT poster FROM posts WHERE pid = ?;", (pid,),
            )
            conn.commit()
            row = c.fetchone()
            #Prints out the badges
            post_poster = row[0]
            print("You may pick a badge from the following: ")
            c.execute("SELECT * FROM badges;")
            conn.commit()
            row = c.fetchone()
            print(row.keys())
            rows = c.fetchall()
            for each in rows:
                print(each["bname"], each["type"])
            given_badge = input("Which badge would you like to give? ")
            #Asks the user to pick a badge
            c.execute("SELECT * from badges where lower(bname) = lower(?);", (given_badge,),)
            #If the user types a badge that is not in the database
            if c.fetchone() is None:
                print("You've written an invalid answer.")
            else:
                try:
                    #Inserts the badge into ubadge table
                    c.execute("INSERT INTO ubadges VALUES (?, ?, ?);", (post_poster, today, given_badge),)
                    conn.commit()
                    invalid = 0
                except sqlite3.Error as e:
                    print(e)
                    invalid = 1
                finally:
                    #If the invalid is 1, returns to main menu without any insertion
                    if invalid == 1:
                        print("Unsuccesful in giving a badge. Returning to the previous page.")
                        return
                    #If invalid is 0, returns to the main menu
                    else:
                        print("Badge has been given successfully. Returning to the previous page.")
                        return

def post_action_tag(pid):
    #Asks the user to input a tag for selected post
    tag = input("Enter the tag you want for your selected post: ")
    insertion_success = 0
    with conn:
        c.execute("SELECT COUNT(tag) FROM tags WHERE pid = ?", (pid,))
    row = c.fetchone()
    #Counts the number of tags within the post
    if row[0] == 0:
        with conn:
            try:
                #Update tags table where tags ID is equal to the post ID
                c.execute('''UPDATE tags SET tag = ? WHERE pid = ?;''', (tag, pid),)
                conn.commit()
                insertion_success = 1
            except sqlite3.Error as e:
                print(e)
                insertion_success = 0
            finally:
                #If the insertion was unsuccessful, returns to main menu without any insertion
                if insertion_success == 0:
                    print("Tag assignment unsuccessful, returning to the previous page.")
                    return
                #If the insertion was successful, returns to main menu
                else:
                    print("Tag assignment successful, returning to the previous page.")
                    return
    else:
        
        with conn:
            try:
                #Inserts the tag into tag table
                c.execute("INSERT INTO tags VALUES(?, ?);", (pid, tag), )
                conn.commit()
                insertion_success = 1
            except sqlite3.Error as e:
                print(e)
                insertion_success = 0
            finally:
                #If the insertion was unsuccessful, returns to main menu without any insertion
                if insertion_success == 0:
                    print("Tag assignment unsuccessful, returning to the previous page.")
                    return
                #If the insertion was successful, returns to main menu
                else:
                    print("Tag assignment successful, returning to the previous page.")
                    return

def post_action_edit(pid):
    #Asks the user to enter new title and body for selected post
    print("To edit this post, please enter a new title and body.")
    title = input("Enter the new title: ")
    body = input("Enter the new body: ")
    update_success = 0
    with conn:
        try:
            #Updates the post table 
            c.execute("UPDATE posts SET title = ?, body = ? WHERE posts.pid = ?;", (title, body, pid), )
            conn.commit()
            update_success = 1
        except sqlite3.Error as e:
            print(e)
            update_success = 0
        finally:
            #If update was successful, returns to main menu
            if update_success == 1:
                print("Update successful, returning you to the previous page.")
                return
            #If the update was unsuccessful, returns to main menu without any insertion
            else:
                print("Update unsuccessful, returning you to the previous page.")
                return


def search_post(userID):
    print("Hi here you can provide one keyword and the system should retrieve all posts that contain atleast one keyword")
    #Asks the user to enter a keyword to see the posts that have matched the keyword
    response = input("Enter a keyword: ")
    values = response.split()


    print('')

    try:
        with conn:
            #Checks for all the posts that have the keyword within the title and body
            pid_mentions = set()
            for value in values:
                c.execute('''SELECT p.pid, COUNT(p.title) as num
                        FROM posts p, tags t
                        WHERE (lower(p.title) LIKE  (?)
                        OR    lower(p.body)  LIKE  (?)
                        OR    lower(t.tag) LIKE   (?))
                        AND   p.pid = t.pid
                        GROUP BY p.pid
                        ORDER BY num DESC;
                        ''',  ('%'+value+'%','%'+value+'%','%'+value+'%'),
                        )
                        
                conn.commit()
                
                
                rows = c.fetchall()
                
                    
            
                for pid, num in rows: pid_mentions.add(pid)

                if len(pid_mentions) == 0:
                    print("No results found from your keywords.\nReturning to the previous page.You can come back again from there and enter a keyword that returns results.")
                    return
                    
            
            #Counts the amount of votes and answers(if question) the post has
            c.execute('''
                SELECT p.pid, p.pdate, p.title, p.body, p.poster, ifnull( posts_votes.num_votes,0), ifnull(posts_answers.num_answers,0)
                    FROM(posts p

                    LEFT OUTER JOIN 

                    (SELECT p.pid, COUNT(DISTINCT(v.pid)) as num_votes
                    FROM posts p, questions q, votes v, answers a
                    WHERE p.pid = v.pid
                    AND   (p.pid = q.pid OR p.pid = a.pid)
                    GROUP BY p.pid) posts_votes ON p.pid = posts_votes.pid

                    LEFT OUTER JOIN

                    (SELECT p.pid, COUNT(*) as num_answers
                    FROM posts p, answers a, questions q
                    WHERE  p.pid = q.pid 
                    AND   a.qid = q.pid 
                    GROUP BY p.pid) posts_answers ON p.pid = posts_answers.pid);''',

                )
            conn.commit()

            post_q_data = {}
            info = c.fetchall()
            #Takes every value and put it into a dictionary 
            for pid,pdate,title,body,poster,num_votes,num_answers in info:
                post_q_data[pid] = [pid, pdate,title,body,poster,num_votes,num_answers]



            
            counter = 0
            loop_breaker = 0
            
            #Prints out every post with the the id, the title, the poster, the amount of votes and the amount of answers from the dict
            for pid in pid_mentions:#pid_mentions
                if pid in post_q_data:
                    if (counter % 5 != 0) or counter == 0:
                        print(' post_id: '+post_q_data[pid][0] +'\n',
                             'date: '+ post_q_data[pid][1] +'\n', 'title: '+post_q_data[pid][2]+ '\n', 'body: '+post_q_data[pid][3] +'\n', 'poster: '+post_q_data[pid][4]+'\n', 'num_votes: '+ str(post_q_data[pid][5])+'\n', 'num_answers'+ str(post_q_data[pid][6])+'\n')
                        print('--------------------------------------------')
                        counter = counter + 1
                        

                    else:
                        while True:
                            #If there are more than 5 posts with matching keyword
                            response = input("Would you like to see another 5 results? Y/N ")
                            response = response.upper()
                            #If user enters Y, the program prints out another 5 posts with the matching keyword 
                            if response == 'Y':
                                print("OK. Loading...")
                                print('')
                                print(' post_id: '+post_q_data[pid][0] +'\n',
                                    'date: '+ post_q_data[pid][1] +'\n', 'title: '+post_q_data[pid][2]+ '\n', 'body: '+post_q_data[pid][3] +'\n', 'poster: '+post_q_data[pid][4]+'\n', 'num_votes: '+ str(post_q_data[pid][5])+'\n', 'num_answers'+ str(post_q_data[pid][6])+'\n')
                                print('--------------------------------------------')
                                counter = counter + 1
                                break
                            #If the user enters N, the program keeps the original 5 posts
                            elif response == 'N':
                                print("OK. Nevermind.")
                                loop_breaker = 1
                                break
                            else:
                                #If user's input is not y or n, it is an invalid input
                                print("Invalid input.")
                        if loop_breaker == 1:
                            break
                                    
                                    
            
            counter_saved = counter
           
            print('')
            print('Checking if you are a privileged user(s): ')
            #Checks if the user is a prvilieged user

            c.execute('''SELECT uid from privileged where uid = ?;''', (userID,),)          
            conn.commit()
            #If the user is a normal user
            if c.fetchone() is None:
                print(" ")
                print("Normal user")

                print("You are now in the normal user menu: ")
                print("You can do a few things here:\n 1) post_action_answer\n 2) post_action_vote\n ")

                while True:
                    print("Type quit if you'd like to leave.")
                    counter = counter_saved    
                    #Asks the user to enter in the post they want to select
                    response = input("enter which post you would like to select: ")
                    response = response.lower()
                    valid = 0
                    pid = 0
                    while valid == 0 and counter >= 0:
                        for pid in pid_mentions:
                            if pid in post_q_data:
                                
                                    
                                    if post_q_data[pid][0] == response:
                                        valid = 1
                                    counter = counter - 1
                    
                    #Checks if the inputted post is in the dict
                    #If the post is within the dictionary            
                    if valid == 1:
                        print("We have found your post. You can leave by typing quit")
                        #User enters what action they want 
                        user_response = input("Please enter what you want to do: ")
                        user_response = user_response.upper()
                        if user_response == '1':
                            #Checks if the post selected is a question or answer
                            #If it is a question, system runs post_action_answer function                            
                            try:
                                c.execute("SELECT * from questions WHERE pid = ?;", (response,),)
                                if c.fetchone() is not None:
                                    post_action_answer(userID, response)
                                else:
                                    print("You've selected an answer. Please try again.")
                            except sqlite3.Error as e:
                                print(e)
                                print("Error please try again.")
                                        
                        elif user_response == '2':
                            #Inputs a vote into the selected post
                            post_action_vote(response, userID)

                        elif user_response == 'QUIT':
                            print("Leaving....")
                            return 
                        #If the user enters anything that is not part of the options
                        else:
                            print("Invalid user input. Please enter a valid option.")

                    elif valid == 0 and response == "quit":
                        print("Leaving...")
                        return
                    elif valid == 0 and response != "quit":
                        print("We couldn't find your post please try again.")

            else:
                print(" ")
                print("privileged")
                #If the user is a privileged user
                print("You are now in the privileged menu:")
                print("You can do a few things here:\n 1) post_action_answer\n 2) post_action_vote\n 3)post_action_mark\n 4) post_action_badge\n 5) post_action_tag\n 6) post_action_edit\n")



                        
                
                while True:
                    print("Type quit if you'd like to leave.")
                    #Asks the user to enter a post
                    counter = counter_saved    
                    response = input("enter which post you would like to select: ")
                    response = response.lower()
                    valid = 0
                    while valid == 0 and counter >= 0:
                        for pid in pid_mentions:
                            if pid in post_q_data:
                                if post_q_data[pid][0] == response:
                                    valid = 1
                                counter = counter - 1
                    #If the post is within the dictionary 
                    if valid == 1 and response != "quit":
                        print("We have found your post. You can leave by typing quit")
                        user_response = input("Please enter what you want to do: ")
                        user_response = user_response.upper()

                        if user_response == '1':
                            try:
                                #Checks if the post selected is a question or answer
                                #If it is a question, system runs post_action_answer function                                 
                                c.execute("SELECT * from questions WHERE pid = ?;", (response,),)
                                if c.fetchone() is not None:
                                    post_action_answer(userID, response)
                                else:
                                    print("You've selected an answer. Please try again.")
                            except sqlite3.Error as e:
                                print(e)
                                print("Error please try again.")
                        elif user_response == '2':
                            #Inputs a vote into the selected post
                            post_action_vote(response, userID)

                        elif user_response == '3':
                            try:
                                #Checks if the post is a question or answer
                                c.execute("SELECT * from answers WHERE pid = ?;", (response,),)
                                if c.fetchone() is not None:
                                    #Marks the answer as accepted answer
                                    post_action_accepted(response)
                                else:
                                    print("You've selected a question. Please try again.")
                            except sqlite3.Error as e:
                                print(e)
                                print("Error please try again.")

                        elif user_response == '4':
                            #User must enter badge name and type that is attached to the selected post
                            post_action_give_badge(response)

                        elif user_response == '5':
                            #User must enter a tag to be attached to the selected post
                            post_action_tag(response)

                        elif user_response == '6':
                            #User can edit the selected post by changing the title and body
                            post_action_edit(response)

                        elif user_response == 'QUIT':
                            #If user enters quit, the program returns user to login_menu
                            print("Leaving...")
                            return 

                        else:
                            #If user enters anything that is not part of the options, system asks the user to enter a valid option
                            print("Invalid user input. Please enter a valid option or quit.")
                    
                    #If user enters quit
                    elif response == "quit" and valid == 0:
                        print("Leaving...")
                        return
                    #If the post was not found or the user does not enter in quit
                    elif valid == 0 and response != "quit":
                        print("Could not find selected post. Try again from displayed results before or quit.")
 

    except sqlite3.Error as e:
        print(e)
    finally:
        print("trying!")




login_menu()


