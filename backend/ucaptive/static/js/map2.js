function initialize() {

    //Map parametrs
    var mapOptions = {
		zoom: 10,
		mapTypeId: google.maps.MapTypeId.TERRAIN,
		scrollwheel: false,
		center: new google.maps.LatLng(44.917406, -110.249240),
		disableDefaultUI: true
    }
    //map
	var map = new google.maps.Map(document.getElementById('page-map'), mapOptions);

    //category
    var home = 'img/icon/home.png';
    var animal = 'img/icon/animal.png';
    var road = 'img/icon/road.png';
    var star = 'img/icon/star.png';
    var eco = 'img/icon/eco.png';

    //positions
    var point1 = new google.maps.LatLng(45.411124, -110.662561);
    var point2 = new google.maps.LatLng(45.206151, -110.914897);
    var point3 = new google.maps.LatLng(45.135480, -111.102337);
    var point4 = new google.maps.LatLng(45.011108, -110.870600);
    var point5 = new google.maps.LatLng(44.913818, -110.999146);
    var point6 = new google.maps.LatLng(44.741163, -111.082270);
    var point7 = new google.maps.LatLng(45.076732, -110.269594);
    var point8 = new google.maps.LatLng(45.021807, -110.391260);
    var point9 = new google.maps.LatLng(44.791828, -110.411690);
    var point10 = new google.maps.LatLng(44.690176, -110.439270);
    var point11 = new google.maps.LatLng(45.249282, -109.846294);
    var point12 = new google.maps.LatLng(45.157802, -109.968748);
    var point13 = new google.maps.LatLng(45.068906, -109.794375);
    var point14 = new google.maps.LatLng(45.015917, -109.576608);
    var point15 = new google.maps.LatLng(44.930559, -109.692855);
    var point16 = new google.maps.LatLng(44.857310, -109.826627);
    var point17 = new google.maps.LatLng(44.655374, -109.471220);
    var point18 = new google.maps.LatLng(44.546470, -109.654201);

    //markers
    var marker1 = new google.maps.Marker({
        position: point1,
        map: map,
        icon: star,
        title: "point1"
    });
    var marker2 = new google.maps.Marker({
        position: point2,
        map: map,
        icon: road,
        title: "Uluru (Ayers Rock)"
    });
    var marker3 = new google.maps.Marker({
        position: point3,
        map: map,
        icon: eco,
        title: "Uluru (Ayers Rock)"
    });
    var marker4 = new google.maps.Marker({
        position: point4,
        map: map,
        icon: animal,
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
        icon: home,
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
    var marker9 = new google.maps.Marker({
        position: point9,
        map: map,
        icon: star,
        title: "Uluru (Ayers Rock)"
    });
    var marker10 = new google.maps.Marker({
        position: point10,
        map: map,
        icon: road,
        title: "Uluru (Ayers Rock)"
    });
    var marker11 = new google.maps.Marker({
        position: point11,
        map: map,
        icon: road,
        title: "point1"
    });
    var marker12 = new google.maps.Marker({
        position: point12,
        map: map,
        icon: animal,
        title: "Uluru (Ayers Rock)"
    });
    var marker13 = new google.maps.Marker({
        position: point13,
        map: map,
        icon: eco,
        title: "Uluru (Ayers Rock)"
    });
    var marker14 = new google.maps.Marker({
        position: point14,
        map: map,
        icon: star,
        title: "Uluru (Ayers Rock)"
    });
    var marker15 = new google.maps.Marker({
        position: point15,
        map: map,
        icon: eco,
        title: "Uluru (Ayers Rock)"
    });
    var marker16 = new google.maps.Marker({
        position: point16,
        map: map,
        icon: animal,
        title: "Uluru (Ayers Rock)"
    });
    var marker17 = new google.maps.Marker({
        position: point17,
        map: map,
        icon: road,
        title: "Uluru (Ayers Rock)"
    });
    var marker18 = new google.maps.Marker({
        position: point18,
        map: map,
        icon: home,
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