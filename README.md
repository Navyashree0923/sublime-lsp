# Camel LSP client for Sublime

The idea is to leverage the [Sublime LSP package](https://github.com/tomv564/LSP).

## Download Sublime

Download from [SublimeText 4 page](https://www.sublimetext.com/download)

# Camel Language Server Support Demo for XML

For instance, code completion for Camel XML.

![Demo](images/xmlsublime.gif)

# Camel Language Server Support Demo for JAVA

For instance, code completion for Camel JAVA.
![Demo](images/javasublime.gif)


## Install LSP plugin

- Tools -> Command palette... -> Package Control: Install Package
- Tools -> Command palette... -> Install LSP

## Configure LSP plugin for Camel

- Download Camel LSP server jar from (https://jar-download.com/artifacts/com.github.camel-tooling/camel-lsp-server/1.6.0/source-code)
- Preferences: Package Setting -> LSP Settings
- fill with updated path to the camel-lsp-server jar
```json
{

	"clients":
	{
		"Camel":
		{
			"command":
			[
				"java",
				"-jar",
				"PATH/TO/camel-lsp-server-1.6.0.jar"
			],
			"enabled": true,
			"languages": [
				{
					"selector": "text.xml",
					"priority_selector": "text.xml",
				},
				{
					"selector": "source.java",
					"priority_selector": "source.java",
				}
			],
		},
	},
}
```
## Inside LSP-lemminx.sublime-settings for XML.
- Tools -> Command palette... -> Prefernces:LSP-lemminx settings
- Tools -> LSP:Enable package server lemminx both Globally and in Project.
```
{
	"ignored_packages":["Vintage"]
}
```
## Inside LSP-jdtls.sublime-settings for Java.
- Tools -> Command palette... -> Prefernces:LSP-jdtls settings
- Tools -> LSP:Enable package server jdtls both Globally and in Project.
```
{
		"version": "1.12.0-202206011637",
		"enabled": true,
}
```
Enjoy the Completion of Camel URI in Sublime.
