/* globals Chart:false, feather:false */

(function () {
    "use strict";
  
    feather.replace()
  
  })()

    // 초기 사용자 id 및 이름 가져오기
    $.ajax({
        url: "{% url 'index' %}",
        type: 'GET',
        success: function (result) {
            $('#userid').text(result.user.userid);
            $('#username').text(result.user.username);
            $('#ps_name').text(result.user.userid);

            for (var i in result.storage) {
                if (result.storage[i].master) {
                    var temp = "<h3><a href='/movetots?name=" + result.storage[i].storage_name + "'>" + result.storage[i].storage_name + " [" + result.storage[i].master + "]</a></h3>";
                } else {
                    var temp = "<h3><a href='/movetots?name=" + result.storage[i].storage_name + "'>" + result.storage[i].storage_name + "</a></h3>";
                }
                $('#storagelist').append(temp);
            }
        },
        error: function (request, status, error) {
            alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        }
    });

    // personal storage 문구 클릭 액션
    $('#ps').click(function () {
        location.href = "{% url 'personal_storage' %}";
    });

    // team storage list 문구 클릭 액션
    $('#ts_list').click(function () {
        location.href = "{% url 'team_storage_list' %}";
    });  
  