const VideoControl = {
  init(video) {
    const experiment = video.getAttribute('data-experiment');
    WebAPI.getPlaybackState(experiment);
  },
  getAll(container = document.body) {
    return container.querySelectorAll('.js-video-control');
  },
};

const WebAPI = {
  init(host) {
    this.socket = new WebSocket(`ws://${host}/ws/video`);
    this.socket.onopen = function connected() {
      const videos = VideoControl.getAll();
      for (let i = 0; i < videos.length; i += 1) {
        VideoControl.init(videos[i]);
      }
    };
    this.socket.onmessage = function parseMessage(e) {
      const data = JSON.parse(e.data);
      switch (data.command) {
        case 'play':
          break;
        default:
          throw new Error('Unknown command');
      }
    };

    this.socket.onclose = function socketError() {
      throw new Error('WebAPI socket closed unexpectedly');
    };
  },
  getPlaybackState(experiment) {
    this.socket.send(JSON.stringify({
      type: 'video.getPlaybackState',
      experiment,
    }));
  },
};

WebAPI.init(window.location.host);
