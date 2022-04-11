function deletePost(postId) {
    fetch("/delete-post", {
      method: "POST",
      body: JSON.stringify({ postId: postId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }
  function banUser(userId) {
    fetch("/ban-user", {
      method: "POST",
      body: JSON.stringify({ userId: userId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }