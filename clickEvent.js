$("#forward").on("click", function () {
  socket.emit("publish", {
    topic: "emqtt",
    message: "a"
  });
});

$("#back").on("click", function () {
  socket.emit("publish", {
    topic: "emqtt",
    message: "d"
  });
});

$("#left").on("click", function () {
  socket.emit("publish", {
    topic: "emqtt",
    message: "b"
  });
});

$("#right").on("click", function () {
  socket.emit("publish", {
    topic: "emqtt",
    message: "c"
  });
});

$("#circle").on("click", function () {
  socket.emit("publish", {
    topic: "emqtt",
    message: "e"
  });
});

$("#follow").on("click", function () {
  socket.emit("publish", {
    topic: "emqtt",
    message: "f"
  });
});

$("#emergency").on("click", function () {
  socket.emit("publish", {
    topic: "emqtt",
    message: "s"
  });
});

$("#submitSpeed").on("click", function () {
  if ($("#inputSpeed").val()) {
    let data = $("#inputSpeed").val() + "g";
    socket.emit("publish", {
      topic: "emqtt",
      message: data
    });
  }
});