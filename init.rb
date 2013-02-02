require 'redmine'

Redmine::Plugin.register :redmine_gitadmin do
  name 'Redmine Gitadmin plugin'
  author 'Piyush Bansal'
  description 'This is a plugin for Redmine'
  version '0.0.1'
	permission :new_repo, { :gitadmin => [:new] }
    	permission :view_git, { :gitadmin => [:index]}, :public => true
menu :project_menu, :gitadmin, { :controller => 'gitadmin', :action => 'index' }, :caption => 'Git Admin', :after => :issues, :param => :project_id


end



