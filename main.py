


from views.main_view import MainView
from controllers.player_controller import PlayerController

def main():

    view = MainView()
  
    controller = PlayerController(view)  

    controller.auto_load_playlist()

    view.run()
if __name__=="__main__":
    main()