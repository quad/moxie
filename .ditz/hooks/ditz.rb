Ditz::HookManager.on :after_add do |project, config, issues|
  issues.each do |issue|
    `git add #{issue.pathname}`
  end
end

Ditz::HookManager.on :after_delete do |project, config, issues|
  issues.each do |issue|
    `git rm #{issue.pathname}`
  end
end

Ditz::HookManager.on :after_update do |project, config, issues|
  issues.each do |issue|
    `git add #{issue.pathname}`
  end
end
