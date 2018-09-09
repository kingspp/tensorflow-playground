$( document ).ready(function() {
      $(document).on('click', '.open-popup-link',function(){
          var popupSRC = $(this).next("div");
          $.magnificPopup.open({
              items: {
                  src: popupSRC,
              },
              type: 'inline'
          });
      });
  });