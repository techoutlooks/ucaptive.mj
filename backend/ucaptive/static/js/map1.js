function initialize() {

    //Map parametrs
    var mapOptions = {
		zoom: 9,
		mapTypeId: google.maps.MapTypeId.TERRAIN,
		scrollwheel: false,
		center: new google.maps.LatLng(44.917406, -110.249240),
		disableDefaultUI: true
    }
    //map
	var map = new google.maps.Map(document.getElementById('h-map'), mapOptions);

    //category
    var marker = 'img/icon/marker.png';
    var animal = 'img/icon/animal.png';
    var road = 'img/icon/road.png';
    var star = 'img/icon/star.png';
    var eco = 'img/icon/eco.png';

    //positions
    var point1 = new google.maps.LatLng(44.917406, -110.249240);
    var point2 = new google.maps.LatLng(45.449688, -110.322610);
    var point3 = new google.maps.LatLng(45.234823, -110.062557);
    var point4 = new google.maps.LatLng(45.140814, -110.903568);
    var point5 = new google.maps.LatLng(44.858160, -109.787686);
    var point6 = new google.maps.LatLng(44.660095, -110.929390);
    var point7 = new google.maps.LatLng(44.628950, -110.404623);
    var point8 = new google.maps.LatLng(44.387981, -109.644142);

    //markers
    var marker1 = new google.maps.Marker({
        position: point1,
        map: map,
        icon: marker,
        title: "point1"
    });
    var marker2 = new google.maps.Marker({
        position: point2,
        map: map,
        icon: animal,
        title: "Uluru (Ayers Rock)"
    });
    var marker3 = new google.maps.Marker({
        position: point3,
        map: map,
        icon: star,
        title: "Uluru (Ayers Rock)"
    });
    var marker4 = new google.maps.Marker({
        position: point4,
        map: map,
        icon: eco,
        title: "Uluru (Ayers Rock)"
    });
    var marker5 = new google.maps.Marker({
        position: point5,
        map: map,
        icon: animal,
        title: "Uluru (Ayers Rock)"
    });
    var marker6 = new google.maps.Marker({
        position: point6,
        map: map,
        icon: star,
        title: "Uluru (Ayers Rock)"
    });
    var marker7 = new google.maps.Marker({
        position: point7,
        map: map,
        icon: road,
        title: "Uluru (Ayers Rock)"
    });
    var marker8 = new google.maps.Marker({
        position: point8,
        map: map,
        icon: eco,
        title: "Uluru (Ayers Rock)"
    });
	
  var styles = [
  {
    stylers: [
      { hue: "#30631B" },
      { saturation: -60 }
    ]
  },{
    featureType: "water",
    stylers: [
      { hue: "#A5C8FF" },
      { saturation: 100 }
    ]
  }
];

map.setOptions({styles: styles});


}
google.maps.event.addDomListener(window, 'load', initialize);	
