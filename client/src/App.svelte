<script>
  import { onMount, tick } from "svelte";
  import { debounce } from "throttle-debounce";

  export let path;

  let completion = "";
  let phrase = "Dear ";
  let showCopySuccess = false;
  let model;
  let inputElement;

  const handleTyping = (event) => {
    const key = event.keyCode || event.charCode;
    if (key == 13) {
      event.preventDefault();
      acceptCompletion();
      return;
    }
    if (key < 48 || key > 90) {
      // Not a-z0-9
      return;
    }
    completion = "";
    fetchCompletion();
  };

  async function acceptCompletion() {
    phrase = phrase + completion;
    completion = "";
    await tick();
    setCursor();
  }

  const fetchCompletion = debounce(1500, () => {
    completion = "...";
    const uriPhrase = encodeURI(phrase);
    fetch(
      `https://nedk6qxpi5.execute-api.us-east-1.amazonaws.com/deployed/completion?type=${model}&phrase=${uriPhrase}`
    )
      .then((response) => response.json())
      .then((data) => {
        completion = data.completion;
      });
  });

  function setCursor() {
    let range, selection;
    range = document.createRange(); // Create a range (a range is a like the selection but invisible)
    range.selectNodeContents(inputElement); // Select the entire contents of the element with the range
    range.collapse(false); // Collapse the range to the end point. false means collapse to end rather than the start
    selection = window.getSelection(); // Get the selection object (allows you to change selection)
    selection.removeAllRanges(); // Remove any selections already made
    selection.addRange(range); // Make the range you have just created the visible selection
  }

  function copyText() {
    const text = phrase + completion;
    navigator.clipboard.writeText(text).then(
      () => {
        console.log("Copying to clipboard was successful! Woo!");
        showCopySuccess = true;
        console.log(showCopySuccess);
        setTimeout(() => (showCopySuccess = false), 3000);
      },
      (err) => alert("Sorry, could not copy to clipboard.")
    );
  }

  onMount(() => {
    setCursor();
  });
</script>

<main>
  <section>
    <label for="model">Choose a model:</label>
    <select bind:value={model} name="model" id="model">
      <option value="shakespeare001">William Shakespeare (Hamlet)</option>
      <option value="trumptweets001">@realdonaldtrump (all tweets)</option>
      <option value="dccc001">DCCC supporter emails </option>
      <option value="gopaz001"
        >Republican Party of Arizona supporter emails
      </option>
      <option value="kjv001">King James Version Bible</option>
    </select>
    <br />
    <br />

    <p>
      Compose an email to a friend in the box below. Press <em>enter</em> to accept
      suggestions.
    </p>
    <section class="composing-area" on:click={setCursor}>
      <span
        bind:this={inputElement}
        contenteditable="true"
        bind:innerHTML={phrase}
        class="input-block"
        on:click|stopPropagation
        on:keydown={handleTyping}
      />
      {#if completion !== ""}
        <spon class="completion-text">{completion} ⏎</spon>
      {/if}
    </section>
    <br />
    <button on:click={copyText}>
      <i class="gg-copy" />
      {#if showCopySuccess}
        <i class="gg-check" />
      {/if}
    </button>
  </section>

  <section>
    <h2>Ask Me Anything</h2>
    <h3>What's your point here?</h3>
    <p>I think text autocomplete is low-grade mind control.</p>
    <h3>Mind control? Isn't that a little dramatic?</h3>
    <p>
      Gmail <a
        href="https://www.blog.google/products/gmail/subject-write-emails-faster-smart-compose-gmail/"
      >
        suddenly starting finishing the thoughts</a
      >
      of its
      <a
        href="https://www.cnbc.com/2019/10/26/gmail-dominates-consumer-email-with-1point5-billion-users.html"
      >
        1.5 billion users</a
      >. It's hard to be hyperbolic when talking about something running at that
      scale.
    </p>
    <h3>
      But Google says that Gmail's suggestions personalized to me. Aren't they
      based on what I've thought in the past?
    </h3>
    <p>Would you know if they weren't?</p>
    <h3>But creating an autocomplete model requires special expertise and careful use of advanced technology, right?</h3>
    <p>
      Not really. I've studied machine learning, but I'm not a deep learning
      guru. I made these autocomplete models by copying <a
        href="https://colab.research.google.com/github/yashk2810/tensorflow/blob/005799649aae3fe4a01a8e69cf88ebbcd86ca8f0/tensorflow/contrib/eager/python/examples/generative_examples/text_generation.ipynb"
      >
        a recursive neural network tutorial from Google.</a
      >
      using a pretty standard gaming PC.
      <a
        href="https://www.technologyreview.com/2020/07/20/1005454/openai-machine-learning-language-generator-gpt-3-nlp/"
        >The really advanced stuff</a
      > is much more powerful.
    </p>
    <h3>What should I do?</h3>
    <p>
      <a
        href="https://support.google.com/mail/answer/9116836?hl=en&co=GENIE.Platform%3DDesktop"
        >Turn off Smart Compose in Gmail</a
      >. Think your own thoughts.
    </p>
	<h3>Can we chat?</h3>
	<p>Sure! Email me: brady.hurlburt [at] pm.me</p>
  </section>
</main>

<style>
  main {
    padding: 1em;
    max-width: 640px;
    margin: 0 auto;
  }

  .composing-area {
    text-align: left;
    border-style: solid;
    border-color: grey;
    padding: 1rem 0.5rem 1.5rem 0.5rem;
  }

  .input-block {
    padding: 0 0.5rem 0 0;
    outline-style: none;
  }

  .completion-text {
    background-color: aquamarine;
  }

  @media (max-width: 720px) {
    main {
      max-width: none;
    }
  }
</style>
