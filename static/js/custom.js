// import * as pg from "./pgbar"
// import * as jqx from "./../node_modules/jqwidgets-scripts";



$(document).on("mouseup", function (e) {
  var button = $("#searchButton");

  if (!button.is(e.target) && button.has(e.target).length === 0) {
    $("#results").removeClass("z-10");
  }
});

function upload_event(obj) {
  var current_event_counter = parseInt(
    $("#how-many-times-clicked").prop("value")
  );

  if (
    current_event_counter != 0 &&
    $("#load-txt").html() == "VIDEO YÜKLƏNDİ! TƏSTİQLƏ"
  ) {
    bar.set(0);
    $("#load-txt").html("YÜKLƏNİR... GÖZLƏYİN");
    $("#video_submit_btn").attr("class", function (i, origValue) {

      return origValue.replace("blinking-button", "");
    }).attr('disabled', true);
  }

  var obj_id = "#" + obj.id;
  var filename = $(obj_id)[0].files[0].name;
  var new_tag = $(
    '<p class="mt-2 text-xs tracking-wide text-gray-500 dark:text-gray-400" id="filename_custom"></p>'
  ).text(filename);

  if ($("#filename_custom").length) {
    filename = $(obj_id)[0].files[0].name;

    $("#filename_custom").html(filename);
  } else {
    $(obj_id).after(new_tag);
  }

  $("#video_submit_btn").attr("disabled", true);
  $("#underline_select").attr("disabled", true);
  $("#customCarRegNumber").attr("disabled", true);
  sendChunk(0, 1, generateUUID(), 1);

  $("#how-many-times-clicked").attr(
    "value",
    (current_event_counter + 1).toString()
  );
}

["#profile-tab", "#dashboard-tab", "#settings-tab", "#dashboard"].forEach(
  function (item, index) {
    $(item).click(() => {
      if ($("#error_alert_banner").attr("class") == "flex justify-center") {
        $("#error_alert_banner").attr("class", "hidden flex justify-center");
      }

      if ($("#carRes")) {
        $("#carRes").remove();
      }
    });
  }
);

function activate_error_banner(message) {
  if (document.getElementById("file-input").files.length == 0) {
    $("#video_form").one("submit", function (e) {
      e.preventDefault();
    });
    $("#error_message_text").html(message);
    $("#error_alert_banner").attr("class", "flex justify-center");
  } else {
    $("#error_alert_banner").attr("class", "hidden flex justify-center");
    $("#video_form").submit();
    $("#video_submit_btn").submit();
  }
}

function activate_error_banner_image(message) {
  if ($("#file-input")[0].files.length == 0) {
    $("#image_form").one("submit", function (e) {
      e.preventDefault();
    });
    $("#error_message_text").html(message);
    $("#error_alert_banner").attr("class", "flex justify-center");
  } else {
    $("#error_alert_banner").attr("class", "hidden flex justify-center");
    $("#image_form").submit();
    $("#image_submit_btn").submit();
  }
}

$("#video_submit_btn").click((e) => {
  if ($("#success_alert_banner")) {
    $("#success_alert_banner").hide();
  }
  if ($("#underline_select option:selected").val()) {
    if (window.location.href.includes("/ferqlenme-upload")) {
      activate_error_banner(
        "Zəhmət olmasa avtomobilin fərqlənmə nişanını yükləyin!"
      );
    } else if ($("#error").val()) {
      if (window.location.href.includes("/ferqlenme-upload")) {
        activate_error_banner(
            "Zəhmət olmasa avtomobilin fərqlənmə nişanını yükləyin!"
        );
    }
    else {
      activate_error_banner("Zəhmət olmasa avtomobilin videosunu yükləyin!");
     }
    }

  }

});

$("#image_submit_btn").click(() => {
  if ($("#underline_select option:selected").val()) {
    activate_error_banner_image(
      "Zəhmət olmasa avtomobilin fərqlənmə nişanını yükləyin!"
    );
  } else if ($("#error").val()) {

    activate_error_banner(
        "Zəhmət olmasa avtomobilin fərqlənmə nişanını yükləyin!"
    );

  }
});

const input = document.querySelector('select[name="car_reg_number"]');

if (input) {
  input.addEventListener("invalid", function (event) {
    if (event.target.validity.valueMissing) {
      event.target.setCustomValidity(
        "Zəhmət olmasa avtomobilin qeydiyyat nişanını seçin"
      );
    }
  });

  input.addEventListener("change", function (event) {
    event.target.setCustomValidity("");
  });
}

// $(document).ready(function(){
//   $('#fo_comment').click(function() { $(this).html('Düzəliş etmək üçün redaktə düyməsinə klikləyin!'); });

// });

// const xyz = document.getElementsByName("fo_comment");
//
// xyz.forEach((elem) =>
// {
//   elem.addEventListener('click', () =>
//   {
//     if ($(elem).text() != "Düzəliş etmək üçün redaktə düyməsinə klikləyin!")
//     {
//       const old_comment = $(elem).text()
//       $(elem).html('Düzəliş etmək üçün redaktə düyməsinə klikləyin!');
//
//       console.log($(elem).text());
//     }
//     else
//     {
//       console.log(elem)
//       $(elem).html('');
//     }
//
//   })
// })
//

function sendChunk(offset, iterCount, folderUUID, successfulRequests) {
  var fileInput = document.getElementById("file-input");
  var file = fileInput.files[0];
  var iterQuantity = Math.ceil(fileInput.files[0].size / (1024 * 1024) / 30);

  var x = successfulRequests;

  var chunkSize = 1024 * 1024 * 30;

  var xhr = new XMLHttpRequest();

  xhr.open("POST", "/upload_u");

  xhr.setRequestHeader("Content-Type", "application/octet-stream");
  xhr.setRequestHeader("X-File-Name", file.name);
  xhr.setRequestHeader("X-File-Size", file.size);
  xhr.setRequestHeader("X-Current-Iter", iterCount);
  xhr.setRequestHeader("X-UUID", folderUUID);

  var chunk = file.slice(offset, offset + chunkSize);
  xhr.send(chunk);

  if (iterCount === 1) {
    // append progress bar here
    NProgress.start();

    $("#custom_progress_bar").attr("class", "w-full h-4 mb-4");

    $("#custom_progress_bar").after("<br />");

    $("#dialog-overlay").attr("class", "flex justify-center");
  }

  offset += chunkSize;

  xhr.onerror = function() {

    window.location.href = '/error';
  };

  xhr.onload = function () {
    xhr.onerror = function() {

    console.log('ERROR')
    $("#error_message_text").html('Zəhmət olmasa HƏFTƏ İÇİ YENİDƏN CƏHD EDİN!');
    xhr.abort();
  };
    window.onbeforeunload = confirmExit;
    function confirmExit() {
      return "Fayl yüklənir! Səhifədən tərk edərək fayl yüklənişini dayandıracaqsınız!";
    }
    if (xhr.status === 200) {


      if (offset < file.size) {
        iterCount += 1;
        setTimeout(sendChunk, 5000, offset, iterCount, folderUUID, x);
      }

      else {
        window.onbeforeunload = null;
        $("#info_message").html('"TƏSTİQLƏ" düyməsinə klikləyin!');
        setTimeout("$(\"#video_submit_btn\").attr('disabled', null);", 1000);
        setTimeout("$(\"#underline_select\").attr('disabled', null);", 1000);
        setTimeout("$(\"#error\").attr('disabled', null);", 1000);
        NProgress.done();
      }

      // console.log(iterCount / iterQuantity);
      // bar.animate(Math.floor(iterCount / iterQuantity));

      // if ()
      bar.animate(iterCount / iterQuantity);

      if (iterCount / iterQuantity == 1) {
        setTimeout('$("#load-txt").html("VIDEO YÜKLƏNDİ! TƏSTİQLƏ");', 4000);
        setTimeout(blink, 4000);
      }
    }
  };
}

function blink() {
  $("#video_submit_btn")
    .attr("class", function (i, origValue) {
      return origValue + " blinking-button";
    }).attr('disabled', null)
    .animate(5000);
}

function upload_event_ferqlenme(obj) {
  var obj_id = "#" + obj.id;
  var filename = $(obj_id)[0].files[0].name;
  var new_tag = $(
    '<p class="mt-2 text-xs tracking-wide text-gray-500 dark:text-gray-400" id="filename_custom"></p>'
  ).text(filename);

  NProgress.configure({ easing: "ease", speed: 1000 });
  NProgress.set(0.5);
  NProgress.start();
  if ($("#filename_custom").length) {
    filename = $(obj_id)[0].files[0].name;

    $("#filename_custom").html(filename);
  } else {
    $(obj_id).after(new_tag);
  }

  NProgress.done();
}

function generateUUID() {
  // Public Domain/MIT
  var d = new Date().getTime(); //Timestamp
  var d2 =
    (typeof performance !== "undefined" &&
      performance.now &&
      performance.now() * 1000) ||
    0; //Time in microseconds since page-load or 0 if unsupported
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
    var r = Math.random() * 16; //random number between 0 and 16
    if (d > 0) {
      //Use timestamp until depleted
      r = (d + r) % 16 | 0;
      d = Math.floor(d / 16);
    } else {
      //Use microseconds since page-load if supported
      r = (d2 + r) % 16 | 0;
      d2 = Math.floor(d2 / 16);
    }
    return (c === "x" ? r : (r & 0x3) | 0x8).toString(16);
  });
}

// find mid ... first value
// find how many pages to add (pointers)

function gridSelector() {
  var total_page_count = parseInt($("#num_of_pages").attr("value"));
  var current_page = parseInt(window.location.href.split("=")[1]);

  if (current_page > 4 && current_page - 3 < total_page_count - 3) {
    var left = current_page - 1;
    var mid = current_page;
    var right = current_page + 1;
  }
}

gridSelector();

$("#underline_select").change(function () {
  if ($("#underline_select").val() && !$("#togglebtn").is(":checked")) {
    // $("#underline_select").prop("disabled", true);
    if ($("#success_alert_banner").is(":visible")) {
      $("#success_alert_banner").addClass('hidden')
    }
    $('label[for="file"]').attr(
      "class",
      "block text-sm text-gray-500 dark:text-gray-300"
    );

    $("#video_div").attr(
      "class",
      "relative mx-auto mt-2 p-5 bg-white cursor-pointer border-2 border-gray-300 border-dashed rounded-lg py-6 flex flex-col items-center"
    );

    $("#img_div").attr(
      "class",
      "relative mx-auto mt-2 p-5 bg-white cursor-pointer border-2 border-gray-300 border-dashed rounded-lg py-6 flex flex-col items-center"
    );

    $("#quote_area").attr("class", "max-w-2xl mx-auto");

    $("#approve_btn").attr("class", "flex justify-center");
  } else if ($("#error").val() && $("#togglebtn").is(":checked")) {
    if ($("#success_alert_banner").is(":visible")) {
      $("#success_alert_banner").addClass('hidden')
    }

    if ($("#success_alert_banner").is(":visible")) {
      $("#success_alert_banner").addClass('hidden')
    }
    $('label[for="file"]').attr(
        "class",
        "block text-sm text-gray-500 dark:text-gray-300"
    );

    $("#video_div").attr(
        "class",
        "relative mx-auto mt-2 p-5 bg-white cursor-pointer border-2 border-gray-300 border-dashed rounded-lg py-6 flex flex-col items-center"
    );

    $("#img_div").attr(
        "class",
        "relative mx-auto mt-2 p-5 bg-white cursor-pointer border-2 border-gray-300 border-dashed rounded-lg py-6 flex flex-col items-center"
    );

    $("#quote_area").attr("class", "max-w-2xl mx-auto");

    $("#approve_btn").attr("class", "flex justify-center");
  }

  else {
    $("#progress_bar_div").attr(
      "class",
      "hidden w-full h-4 mb-4 bg-gray-200 rounded-full dark:bg-gray-700"
    );

    if ($("#success_alert_banner").is(":visible")) {
      $("#success_alert_banner").addClass('hidden')
    }

    $('label[for="file"]').attr(
      "class",
      "hidden block text-sm text-gray-500 dark:text-gray-300"
    );
    $("#video_div").attr(
      "class",
      "hidden relative mx-auto mt-2 p-5 bg-white cursor-pointer border-2 border-gray-300 border-dashed rounded-lg py-6 flex flex-col items-center"
    );

    $("#img_div").attr(
      "class",
      "hidden relative mx-auto mt-2 p-5 bg-white cursor-pointer border-2 border-gray-300 border-dashed rounded-lg py-6 flex flex-col items-center"
    );
    $("#quote_area").attr("class", "hidden max-w-2xl mx-auto");

    $("#approve_btn").attr("class", "hidden flex justify-center");
  }
});


// $("#error").change(function () {
//
//
//   if ($("#error").val()) {
//     enableForm()
//   }
//
//   else {
//     disableForm()
//   });

function enableForm() {

  if ($("#success_alert_banner").is(":visible")) {
    $("#success_alert_banner").addClass('hidden')
  }


  $('label[for="file"]').attr(
      "class",
      "block text-sm text-gray-500 dark:text-gray-300"
  );

  $("#video_div").attr(
      "class",
      "relative mx-auto mt-2 p-5 bg-white cursor-pointer border-2 border-gray-300 border-dashed rounded-lg py-6 flex flex-col items-center"
  );

  $("#img_div").attr(
      "class",
      "relative mx-auto mt-2 p-5 bg-white cursor-pointer border-2 border-gray-300 border-dashed rounded-lg py-6 flex flex-col items-center"
  );

  $("#quote_area").attr("class", "max-w-2xl mx-auto");

  $("#approve_btn").attr("class", "flex justify-center");
}


function disableForm() {
  $("#progress_bar_div").attr(
      "class",
      "hidden w-full h-4 mb-4 bg-gray-200 rounded-full dark:bg-gray-700"
  );



  $('label[for="file"]').attr(
      "class",
      "hidden block text-sm text-gray-500 dark:text-gray-300"
  );
  $("#video_div").attr(
      "class",
      "hidden relative mx-auto mt-2 p-5 bg-white cursor-pointer border-2 border-gray-300 border-dashed rounded-lg py-6 flex flex-col items-center"
  );

  $("#img_div").attr(
      "class",
      "hidden relative mx-auto mt-2 p-5 bg-white cursor-pointer border-2 border-gray-300 border-dashed rounded-lg py-6 flex flex-col items-center"
  );
  $("#quote_area").attr("class", "hidden max-w-2xl mx-auto");

  $("#approve_btn").attr("class", "hidden flex justify-center");

}

function activateProgressBar(progress) {
  $("#progress_bar_div").attr(
    "class",
    "w-full h-4 mb-4 bg-gray-200 rounded-full dark:bg-gray-700"
  );

  let now = parseInt(
    $("#progress_bar").attr("style").split("width: ")[1].split("%")[0]
  );

  for (; now <= progress; now++) {
    increment(now);
  }
}

function increment(i) {
  setTimeout(
    '$("#progress_bar").attr("style',
    'width: " + i.toString() + "%")',
    1000
  );
}

if (window.location.pathname == "/") {
  var bar = new ProgressBar.Line(custom_progress_bar, {
    strokeWidth: 4,
    // easing: "easeIn",
    duration: 4000,
    color: "#1C64F2",
    trailColor: "#3e83f980",
    trailWidth: 1,
    svgStyle: { width: "100%", height: "100%" },
  });
}

$(document).ready(navigateAnimvation);

window.addEventListener("popstate", navigateAnimvation);

function navigateAnimvation() {
  const isNavigate = window.location.href.split("#");

  if (isNavigate.length > 1) {
    var $section = $("#" + isNavigate[1]);
    $section
      .removeClass(
        "bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
      )
      .addClass("fade-in");
    window.setTimeout(function () {
      $section.addClass("fade-out");

      window.setTimeout(function () {
        $section.removeClass("fade-in");
        $section.removeClass("fade-out");
        $section.addClass(
          "bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
        );
      }, 400);
    }, 400);
  }
}

function searchCars(thisElem) {
  var data = $(thisElem).prop("value");

  if (data != "" || data) {
    if ($("#carRes").length) {
      // delete all node
      $("#carRes").remove();
    }

    var $newDiv = $(
      '<div id=\'carRes\' class=\'z-10 search-car-results bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white\'> \
      <div id="carStatus" role="status" class="flex justify-center items-center ">\
    <svg aria-hidden="true" class="flex justify-center items-center w-5 h-5 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/><path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/></svg>\
    <span class="sr-only flex justify-center items-center ">Loading...</span>\
    </div>\
    </div>'
    );

    $(thisElem).after($newDiv);

    fetch("/admin/searchCar?carreg=" + data)
      .then((response) => response.json())
      .then((data) => {
        $("#carStatus").remove();

        for (var res in data) {
          $("#carRes").append(
            '\
        <table class="w-full">\
            <tbody id="carResTable">\
            </tbody>\
        </table>'
          );
          if (data[res] != "No such car") {
            if ($(".car-res-trs").length && $("#carResTable").length) {
              $(".car-res-trs").remove();
            }
            for (var listIndex in data[res]) {
              $("#carResTable")
                .append(`<tr onmouseover="backgroundBlue(this)" onmouseout="reset(this)" onclick="selectCar(this, ${data[res][listIndex][1]})" class="clickable-row car-res-trs">
              <th scope="row" class="px-4 py-2 font-medium text-gray-900">
                  ${data[res][listIndex][0]}
              </th>

              
             
              </tr>`);
            }
          } else {
            if ($(".car-res-trs").length && $("#carResTable").length) {
              $(".car-res-trs").remove();
            }

            $("#carResTable")
              .append(`<tr onmouseover="backgroundBlue(this)" onmouseout="reset(this)" class="clickable-row car-res-trs">
              <th scope="row" class="px-4 py-2 font-medium text-gray-900">
                  Avtomobil bazada tapılmadı
              </th>
             
              </tr>`);
          }
        }

        return;
        // Handle the received data
      })
      .catch((error) => {
        console.error("Error:", error);
        // Handle any errors that occurred during the request
      });
  } else {
    if ($("#carRes").length) {
      $("#carRes").remove();
    }
  }
}

function searchApps(data, elem) {
  if (data != "") {
    if ($("#results").length) {
      // delete all node
      $("#results").remove();
    }

    var $newDiv = $(
      '<div id=\'results\' class=\'z-10 search-results bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white\'> \
      <div id="status" role="status" class="flex justify-center items-center ">\
    <svg aria-hidden="true" class="flex justify-center items-center w-5 h-5 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/><path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/></svg>\
    <span class="sr-only flex justify-center items-center ">Loading...</span>\
    </div>\
    </div>'
    );
    var elem = $(elem);

    elem.after($newDiv);

    fetch("/admin/search?carreg=" + data.trim())
      .then((response) => response.json())
      .then((data) => {
        $("#status").remove();

        for (var res in data) {
          if (data[res] != "No such car application") {
            $("#results").append(
              '\
          <table class="w-full">\
              <tbody id="resTable">\
              </tbody>\
          </table>'
            );
            for (var pageLimit in data[res]) {
              var appPath = "/admin?limit=" + pageLimit;

              for (var _enum in data[res][pageLimit]) {
                appPath +=
                  "#" + data[res][pageLimit][_enum]["app-id"].toString();

                $("#resTable")
                  .append(`<tr onmouseover="backgroundBlue(this)" onmouseout="reset(this)" class="clickable-row"  data-href="${appPath}">
              <th scope="row" class="px-4 py-2 font-medium text-gray-900">
                  ${data[res][pageLimit][_enum]["app-company"]}
              </th>
              <td class="px-4 py-2 font-medium text-gray-900">
              ${data[res][pageLimit][_enum]["app-car-reg"]}
              </td>
              <td class="px-4 py-2">
              ${(() => {
                if (data[res][pageLimit][_enum]["app-status"] == "Approved") {
                  return '<p  onmouseover="backgroundBlue(this)" onmouseout="reset(this)" style="color:green">TƏSTİQLƏNİB</p>';
                } else if (
                  data[res][pageLimit][_enum]["app-status"] == "Declined"
                ) {
                  return '<p  onmouseover="backgroundBlue(this)" onmouseout="reset(this)" style="color:red">RƏDD EDİLİB</p>';
                } else {
                  return '<p onmouseover="backgroundBlue(this)" onmouseout="reset(this)"  style="color:blue">YOXLANIŞDA</p>';
                }
              })()}
              </td>
              <td class="px-4 py-2">
              ${(() => {
                if (data[res][pageLimit][_enum]["app-type"] == 1) {
                  return '<p  onmouseover="backgroundBlue(this)" onmouseout="reset(this)">Fərqlənmə nişanı</p>';
                } else if (data[res][pageLimit][_enum]["app-type"] == 2) {
                  return '<p  onmouseover="backgroundBlue(this)" onmouseout="reset(this)">Video reklam</p>';
                } else {
                  return '<p onmouseover="backgroundBlue(this)" onmouseout="reset(this)">Avtomobil silinməsi</p>';
                }
              })()}
              </td>

              <td class="px-4 py-2">
              ${data[res][pageLimit][_enum]["app-applied"]}
              </td>
              </tr>`);

                $(".clickable-row").click(function () {
                  window.location = $(this).data("href");
                });

                appPath = "/admin?limit=" + pageLimit;
              }
            }
          } else {
            // No such car application result (dump an error)
          }
        }

        return;
        // Handle the received data
      })
      .catch((error) => {
        console.error("Error:", error);
        // Handle any errors that occurred during the request
      });
  } else {
    if ($("#results").length) {
      $("#results").remove();
    }
  }
}

function removeResults() {
  if ($("#results").length) {
    // delete all node
    $("#results").remove();
  }
}

function backgroundBlue(elem) {
  $(elem).css("cursor", "pointer");
  $(elem).addClass("bg-blue-500 rounded");
}

function reset(elem) {
  $(elem).removeClass("bg-blue-500 rounded");
}

function selectCar(_this, car_ref_id) {
  // get car reg number from table elem
  var carRegNumber = $(_this).children().html().trim(); // car reg number itself  77BR324

  var carRefElem = $(_this)
    .parent()
    .parent()
    .parent()
    .parent()
    .children("#carRef")[0];

  // update input field's value with car reg number
  carRefElem.value = carRegNumber;

  var currentAppId = carRefElem.name.split("_")[3];

  // carRefElem.name = "car_input_ref_" + car_ref_id.toString();

  $(`input[name=\"car_ref_${currentAppId.toString()}\"]`)[0].value =
    car_ref_id.toString();

  // remove all table nodes
  $("#carRes").remove();
}

function selectAll(elem) {
  // console.log(elem);
  if (elem.checked) {
    Array.from($(".checkbox-table-search")).map((i) => (i.checked = true));
  } else {
    Array.from($(".checkbox-table-search")).map((i) => (i.checked = false));
  }
}

function customCarRegToggle(element){

  disableForm()


  if (element.checked) {
    $("#carRegDropdown").addClass("hidden");
    $("#error").attr('required', '')
    $("#underline_select").removeAttr('required');
    $("#carRegInputBox").removeClass("hidden");
    $("[name='isCustomCarReg']").attr('value', 1)
    // because when type=checkbox is not checked then it's not submitted in the form
    element.value = 1;

    carRegValidator($("#error")[0])
  } else {

    // reset, or enable initial dropdown
    element.value = 0;
    $("[name='isCustomCarReg']").attr('value', 0)
    $("#carRegInputBox").addClass("hidden");
    $("#underline_select").attr('required', '')
    $("#error").removeAttr('required');
    $("#carRegDropdown").removeClass("hidden");

    if ($("#underline_select").val() && !$("#togglebtn").is(":checked")) {
      enableForm()
    }

  }
}

function carRegValidator(elem) {

  try {
    elem.value = elem.value.toUpperCase()
  } catch (e) {
    return
  }


  var inputVal = elem.value
  const re = /^\d{2}[A-Z]{2}\d{3}$/
  var cleanArrOfChildren = new Array()

  getArray($("#carRegInputBox")[0].children).forEach(
      (elem) => elem.nodeName !== "INPUT" ? cleanArrOfChildren.push(
          elem
      ) : null
  )


  if (!inputVal.match(re)) {

    disableForm()

    $("#error").removeClass("bg-green-50 border-green-500 text-green-900 placeholder-green-700 focus:ring-green-500 dark:bg-gray-700 focus:border-green-500 dark:text-green-500 dark:placeholder-green-500 dark:border-green-500")
    $("#error").addClass("bg-red-50 border-red-500 text-red-900 placeholder-red-700 focus:ring-red-500 dark:bg-gray-700 focus:border-red-500 dark:text-red-500 dark:placeholder-red-500 dark:border-red-500")

    cleanArrOfChildren.forEach((el) => $(el).removeClass('hidden'))


  } else {

    $("#error").removeClass("bg-red-50 border-red-500 text-red-900 placeholder-red-700 focus:ring-red-500 dark:bg-gray-700 focus:border-red-500 dark:text-red-500 dark:placeholder-red-500 dark:border-red-500")
    $("#error").addClass("bg-green-50 border-green-500 text-green-900 placeholder-green-700 focus:ring-green-500 dark:bg-gray-700 focus:border-green-500 dark:text-green-500 dark:placeholder-green-500 dark:border-green-500")
    // $("#error").attr("disabled", '')
    cleanArrOfChildren.forEach((el) => $(el).addClass('hidden'))


    enableForm()

  }
}

function getArray(objOfElems) {
  var elems = objOfElems;
  var arr = new Array();
  for (var i = 0; i < elems.length; i++) {
    arr.push(elems[i])
  }
  return arr;
}

$(document).ready(() => {
  $("#underline_select option:first").prop("selected", true);


  if (
      $("#underline_select option:selected").val() &&
      !$("#success_alert_banner").prop("class").includes("hidden")
  ) {
    $("#success_alert_banner").addClass("hidden");
  }

  console.log('Ready')

  customCarRegToggle($("#togglebtn")[0])

  disableForm()

  if ($("#error").val()) {

    $("#error").val("")

  }

});

jQuery(document).ready(
    function() {
      var myPlayers = $('.rtopvideoplayer');
      Object.keys(myPlayers).forEach((key) => {
        myPlayers[key].RTOP_VideoPlayer(
            {
              showControls: true,
              showControlsOnHover: true,
              controlsHoverSensitivity: 3000,
              showScrubber: true,
              showTimer: false,
              showPlayPauseBtn: true,
              showSoundControl: false,
              showFullScreen: false,
              keyboardControls: true,

            }
        );
      })
    }
)