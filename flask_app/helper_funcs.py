from flask_app import app
from flask_app.models import User, List, Card
import matplotlib.pyplot as plt
from datetime import datetime

def make_plot(list_id):
    #make a pie chart using the data from this list
    list_obj = List.query.get(list_id)
    total_cards = len(list_obj.cards)
    if total_cards != 0:
        completed_cards = len(Card.query.filter_by(list_id=list_id, status='Completed').all()) #fetches all the 'Completed' cards lying inside this list
        pending_cards = 0
        current_date = datetime.today().date()
        deadlines_missed = 0
        for card in list_obj.cards:
            if card.status == "Pending" and current_date < card.deadline:
                # a card is considered pending if its status is pending and if current date is less than deadline date
                pending_cards += 1
            elif card.status == "Pending" and current_date > card.deadline:
                # a card is considered 'missed' if its status is pending and if current date is past the deadline date
                deadlines_missed += 1
        
        # Data to plot
        my_data = [completed_cards, pending_cards, deadlines_missed]
        my_labels = 'Completed', 'Pending', 'Deadlines Missed'
        fig, ax = plt.subplots(figsize=(3.5,3.5))
        fig.set_facecolor('#f8f8ff') # set the background color of the pie chart
        colors = ['yellowgreen', 'gold', 'coral'] # colors to be used for the pies

        # Plot the chart
        plt.pie(my_data, colors=colors) #to show percentages use: autopct='%1.1f%%'
        plt.legend(labels=my_labels, loc='upper right')
        plt.axis('equal')
        #each image is of the form "list_{list_id}.jpeg", eg: list_1.jpeg. Each image corresponds to stats about that particular list.
        plt.savefig(f"flask_app/static/images/list_{list_id}.jpeg", dpi=300)
        plt.close()
        return "Chart:"
    else:
        return "This List is empty. Add some cards to view the Stats."

# I want to make this "make_plot" function globally accessible, so I can access it from anywhere
app.jinja_env.globals.update(make_plot=make_plot) #now this make_plot function can be called from within a jinja template

def generate_csv(username):
    # generate a csv file containing data about user's lists and cards
    usr_obj = User.query.filter_by(username=username).first()
    f = open('./flask_app/exported_content.csv', 'w')
    f.write('List ID, List Title, Card ID, Card Title, Card Content, Card Status, Card Deadline\n')
    for lst in usr_obj.lists:
        for card in lst.cards:
            f.write(f'{lst.list_id},"{lst.list_title}",{card.card_id},"{card.card_title}","{card.card_content}",{card.status},{card.deadline}\n')
    f.close()
