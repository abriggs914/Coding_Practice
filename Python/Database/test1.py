Tests.componentTest(function (Components) {
  if (Components.CodeEditor.codeContains('script.py', /new_df\s*=\s*pd\s*.\s*merge\s*(\s*user_data\s*,\s*pop_data\s*)/)) {
    return { pass: true };
  }
  return {
    pass: false,
    errors: {
      friendly: 'Did you copy and paste the merge code?',
      component: 'PersistentCodeEditor'
    }
  };
}, callback);