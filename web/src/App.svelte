<script lang="ts">
  import { onMount } from "svelte";
  import Icon from "svelte-awesome";
  import { globe, caretRight } from "svelte-awesome/icons";
  import Footer from "./components/Footer.svelte";

  let text_input = "";
  let text_input_old = "";
  let last_input = (new Date());
  let translate_en = false;
  let translate_zh = false;
  let translate_ko = false;
  let translate_ja = false;
  let chat_notify = false;
  let logging = "";
  let logging_raw = [];

  function log(msg) {
    logging_raw.unshift(msg);
    while (logging_raw.length > 100) logging_raw.pop();
    logging = logging_raw.join('\n');
  }

  function submit() {
    let data = {
      "text": text_input,
      "translate_en": translate_en,
      "translate_zh": translate_zh,
      "translate_ko": translate_ko,
      "translate_ja": translate_ja,
      "chat_notify": chat_notify,
    };
    log(`submit data=${JSON.stringify(data)}`);
    fetch('/api/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(res => res.json())
    .then(data => {
      log(`success: ${JSON.stringify(data)}`);
    })
    .catch((error) => {
      log(`error: ${error}`);
    });
  }

  function lifeCycle() {
    // text_input = text_input.trim();
    text_input = document.getElementById("T").value.trim();
    if (text_input != text_input_old) {
      text_input_old = text_input;
      last_input = (new Date());
      console.log(text_input, last_input);
    } else if (text_input !== "") {
      if ((new Date()) - last_input > 500) {
        submit();
        text_input = "";
      }
    }
  }

  onMount(() => {
    setInterval(lifeCycle, 200);
  });
</script>

<svelte:head>
  <title>vrc-in</title>
</svelte:head>

<div class="section">
  <div class="container">
    <div class="content">
      <h2 class="subtitle">vrc-in v0.2.0</h2>
      <div class="field">
        <div class="control">
          <textarea class="textarea" placeholder="Text here" id="T" bind:value={text_input}></textarea>
        </div>
        <div class="control">
          <label class="label">翻訳</label>
          <label class="checkbox"><input type="checkbox" bind:checked={translate_en}>en</label>
          <label class="checkbox"><input type="checkbox" bind:checked={translate_zh}>zh</label>
          <label class="checkbox"><input type="checkbox" bind:checked={translate_ko}>ko</label>
          <label class="checkbox"><input type="checkbox" bind:checked={translate_ja}>ja</label>
        </div>
        <div class="control">
          <label class="label">設定</label>
          <label class="checkbox"><input type="checkbox" bind:checked={chat_notify}>通知音</label>
        </div>
      </div>
      <div class="field">
        <div class="control">
          <textarea class="textarea" placeholder="Debug log" bind:value={logging} disabled="disabled"></textarea>
        </div>
      </div>
    </div>
  </div>
</div>

<style global lang="scss">
  @import "main.scss";
</style>
